"""Process ERA5 .grb files
"""

import numpy as np
import pygrib
import pandas as pd
from scipy import interpolate
import utils


class Era5():
    """

    """

    def __init__(self, grb_file, lat_range=None, lon_range=None,
                 site=None, var_names_short=None):
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

        # Extract lat/lon
        lat, lon = self.grb.read(1)[0].latlons()
        self.lat, self.lon = _slice_latlon(lat, lon,
                                           self.lat_range,
                                           self.lon_range)
        # Target lat/lon
        ww3lat, ww3lon = utils.ww3_grid()
        self.target_lat, self.target_lon = _slice_latlon(ww3lat, ww3lon,
                                                         self.lat_range, self.lon_range)

        # Target mask
        self.mask = utils.ww3_mask(self.lat_range, self.lon_range)

        # Number of non-masked output grid points
        self.gridpoints = len(self.target_lat[~self.mask])

        # Variable dictionary
        if var_names_short is None:
            self.var_names_short = utils.var_names_short
        self.vardict = _var_df_dict(self.var_names_short, self.gridpoints)

    def format(self, method="linear"):
        """

        """
        self.method = method
        # Iterate through variables in grb file
        for gm in self.grb:
            # Get full name and short name
            # short name is the variable dict key
            name = gm.name
            sname = gm.shortName
            var_data = _region_data(gm, self.lat_range, self.lon_range)
            print(type(var_data))
            # Interpolate to target lat and lon
            interp_data = _interp_ww3(var_data, self.lon, self.lat,
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
    in_values = variable_data[~variable_data.mask].data
    in_lon = lon[~variable_data.mask].flatten()
    in_lat = lat[~variable_data.mask].flatten()
    in_points = np.zeros(shape=(len(in_lon), 2))
    in_points[:, 0] = in_lon
    in_points[:, 1] = in_lat

    interp_data = interpolate.griddata(
        in_points, in_values, (target_lon, target_lat), method=method)

    return interp_data
