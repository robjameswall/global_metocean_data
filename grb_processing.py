"""Process .grb files and extract data in table format
"""

import numpy as np
import pygrib
import pandas as pd
from scipy import interpolate
import grb_utils as utils


class GrbData(object):
    """

    """

    def __init__(self, grb_file, lat_range=None, lon_range=None,
                 site=None, var_names=None, var_names_short=None):
        self.fn = grb_file
        self.site = site

        if self.site is not None:
            self.lat_range = utils.region_box[self.site]['lat']
            self.lon_range = utils.region_box[self.site]['lon']
        else:
            self.lat_range = lat_range
            self.lon_range = lon_range

        self.site = site
        self.grb = pygrib.open(grb_file)

        # Analysis date
        self.anal_date = self.grb.read(1)[0].analDate
        self.reset_grb()

        # Long variable names
        if var_names is None:
            self.var_names = utils.var_names
        else:
            self.var_names = var_names
            
        # Variable dictionary keys
        if var_names_short is None:
            self.var_names_short = utils.var_names_short
        else:
            self.var_names_short = var_names_short
        
        # Variable dictionary
        # Match each variable to length of
        self.vardict = {}
        for (v, vshort) in zip(self.var_names, self.var_names_short):
            temp_grb = self.grb.select(name=v)[0]
            lat, lon = temp_grb.latlons()
            lat_region, lon_region = _slice_latlon(lat, lon, self.lat_range, self.lon_range)
            
            colnames = _var_col_names_latlons(vshort, lat_region.flatten(), lon_region.flatten())
            self.vardict[vshort] = {
                "name": v,
                "df": pd.DataFrame(columns=colnames),
                "index": list()
            }
    
    def format(self):
        """
        Ignore the target mask, output variables within lat/lon range
        using the mask within each grib. Use lat/lon coords for column
        names; these are now identifiable by position.
        
        """
        self.reset_grb()
        # Iterate through variables in grb file
        for gm in self.grb:
            
            # Get full name and short name
            # short name is the variable dict key
            name = gm.name
            sname = gm.shortName
            
            # Read if variable is in vardict keys
            if sname in self.vardict.keys():

                # Get lat, lon
                lat, lon = gm.latlons()

                # Slice region
                lat, lon = _slice_latlon(lat, lon, self.lat_range, self.lon_range)

                # Get variable data
                var_data = _region_data(gm, self.lat_range, self.lon_range)

                dt = gm.analDate

                # Insert in variable dictionary dataframe
                df_len = len(self.vardict[sname]["df"])
                df = self.vardict[sname]["df"]
                df.loc[df_len] = var_data.flatten()
                self.vardict[sname]["index"].append(dt)
                df.index = self.vardict[sname]["index"]


    def reset_grb(self):
        """
        Reset the pygrib iterator
        """
        self.grb.seek(0)

    def create_df(self):
        """
        Merge dataframes in self.vardict
        """
        df_list = [self.vardict[v]["df"] for v in self.var_names_short]

        self.df = pd.concat(df_list, axis=1, sort=False)


def _slice_latlon(lat, lon, lat_range, lon_range):
    """
    Provide grid of lat/lon and extract values within
    lat/lon range
    """
    mask = (lat >= lat_range[0]) & (lat <= lat_range[1]) & \
           (lon >= lon_range[0]) & (lon <= lon_range[1])

    dim1 = np.any(mask, axis=1).sum()
    dim2 = np.any(mask, axis=0).sum()

    lat_extract = lat[mask].reshape(dim1, dim2)
    lon_extract = lon[mask].reshape(dim1, dim2)

    return lat_extract, lon_extract


def _region_data(gribmessage, lat_range, lon_range):
    """
    Extract data from pygrib gribmessage object
    for lat/lon region
    """

    return gribmessage.data(lat1=lat_range[0], lat2=lat_range[1],
                            lon1=lon_range[0], lon2=lon_range[1])[0]


def _var_col_names_latlons(var_name, in_lat, in_lon):
    cnames = []
    for lat, lon in zip(in_lat, in_lon):
        latstr = "n" if lat < 0 else "p"
        lonstr = "n" if lon < 0 else "p"
        cstr = "{}_lat_{}{}_lon_{}{}".format(var_name, latstr, lat, lonstr, lon)
        cstr = cstr.replace("-", "")
        cstr = cstr.replace(".", "_")
        cnames.append(cstr)
    return cnames
