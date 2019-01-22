"""Process ERA5 .grb files
"""

import numpy as np
import pygrib
import pandas as pd
from scipy import interpolate
import utils


class Era5(object):
    """

    """

    def __init__(self, grb_file, lat_range=None, lon_range=None,
                 site=None, var_names_short=None, ww3=False):
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

        # If ww3 is False; read ww3 mask and lat, lon from
        # saved ww3 file
        if ww3:
            in_ww3_grb = self.grb
        else:
            in_ww3_grb = None

        # Target lat/lon
        ww3lat, ww3lon = utils.ww3_grid(in_ww3_grb)
        self.target_lat, self.target_lon = _slice_latlon(ww3lat, ww3lon,
                                                         self.lat_range, self.lon_range)

        # Target mask
        self.mask = utils.ww3_mask(self.lat_range, self.lon_range,
                                   in_ww3_grb)

        # Number of non-masked output grid points
        self.gridpoints = len(self.target_lat[~self.mask])

        # Variable dictionary
        if var_names_short is None:
            self.var_names_short = utils.var_names_short
        else:
            self.var_names_short = var_names_short
        self.vardict = _var_df_dict(self.var_names_short, self.gridpoints)

    def format(self, method="linear"):
        """

        """
        self.reset_grb()
        self.method = method
        # Iterate through variables in grb file
        for gm in self.grb:
            # Get full name and short name
            # short name is the variable dict key
            name = gm.name
            sname = gm.shortName

            # Get lat,lon
            lat, lon = gm.latlons()

            # Slice region
            lat, lon = _slice_latlon(lat, lon, self.lat_range, self.lon_range)

            var_data = _region_data(gm, self.lat_range, self.lon_range)
            # Interpolate to target lat and lon
            interp_data = _interp_ww3(var_data, lon, lat,
                                      self.target_lon, self.target_lat, self.method)

            # Get non-masked data
            interp_data = interp_data[~self.mask]
            dt = gm.analDate

            # Insert in variable dictionary dataframe
            if len(self.vardict[sname]["name"]) != 0:
                self.vardict[sname]["name"] = name
            df_len = len(self.vardict[sname]["df"])
            df = self.vardict[sname]["df"]
            df.loc[df_len] = interp_data
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


class Ww3(Era5):
    """

    """

    def __init__(self, ww3_file, lat_range=None, lon_range=None,
                 site=None, var_names_short=None):

        if var_names_short is None:
            var_names_short = utils.ww3_var_names_short
        super(Ww3, self).__init__(ww3_file, lat_range, lon_range,
                                  site, var_names_short)

    def format(self):
        """

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

                # Read data within lat/lon range
                var_data = _region_data(gm, self.lat_range, self.lon_range)

                # Get non-masked data
                var_data = var_data[~self.mask]

                # Insert in variable dictiontary dataframe
                dt = gm.validDate
                if len(self.vardict[sname]["name"]) != 0:
                    self.vardict[sname]["name"] = name
                df_len = len(self.vardict[sname]["df"])
                df = self.vardict[sname]["df"]
                df.loc[df_len] = var_data
                self.vardict[sname]["index"].append(dt)
                df.index = self.vardict[sname]["index"]


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


def _var_col_names(n, var_name):
    return ["{}_p{}".format(var_name, i) for i in range(1, n + 1)]


def _var_df_dict(var_names, n):
    var_dict = dict()

    for vn in var_names:
        col_names = _var_col_names(n, vn)
        var_dict[vn] = {
            "name": "",
            "df": pd.DataFrame(columns=col_names),
            "index": list()
        }
    return var_dict


def _interp_ww3(variable_data, lon, lat,
                target_lon, target_lat, method='linear'):
    """
    2d Interpolate variable data located at lon, lat to
    target_lon and target_lat
    """

    # Most data will be in a numpy MaskedArray but some,
    # such as wind component, will not
    if type(variable_data) == np.ma.core.MaskedArray:
        in_values = variable_data[~variable_data.mask].data
        in_lon = lon[~variable_data.mask].flatten()
        in_lat = lat[~variable_data.mask].flatten()
    else:
        in_values = variable_data.flatten()
        in_lon = lon.flatten()
        in_lat = lat.flatten()

    in_points = np.zeros(shape=(len(in_lon), 2))
    in_points[:, 0] = in_lon
    in_points[:, 1] = in_lat

    interp_data = interpolate.griddata(
        in_points, in_values, (target_lon, target_lat), method=method)

    return interp_data
