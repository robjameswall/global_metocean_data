"""Support functions
"""

import numpy
import pygrib

ww3_f = "data/nww3.t00z.grib.grib2.grb"

# Region lat/lon bounding boxes
region_box = {
    "gold_coast": {
        "lat": [-31, -25],
        "lon": [152, 157]
    }
}

# Era5 variable names
var_names = {
    u'10 metre U wind component',
    u'10 metre V wind component',
    u'Mean direction of total swell',
    u'Mean direction of wind waves',
    u'Mean period of total swell',
    u'Mean period of wind waves',
    u'Mean wave direction',
    u'Mean wave direction of first swell partition',
    u'Mean wave direction of second swell partition',
    u'Mean wave period',
    u'Mean wave period based on first moment for swell',
    u'Mean wave period of first swell partition',
    u'Mean wave period of second swell partition',
    u'Significant height of combined wind waves and swell',
    u'Significant height of wind waves'
}

var_names_short = {
    u'10u',
    u'10v',
    u'mdts',
    u'mdww',
    u'mpts',
    u'mpww',
    u'mwd',
    u'mwd1',
    u'mwd2',
    u'mwp',
    u'mwp1',
    u'mwp2',
    u'p1ps',
    u'shww',
    u'swh'
}

# WW3 variable names
ww3_var_names = {
    u"Direction of wind waves"
    u"Mean period of wind waves"
    u"Primary wave direction"
    u"Primary wave mean period"
    u"Secondary wave direction"
    u"Secondary wave mean period"
    u"Significant height of combined wind waves and swell"
    u"Significant height of wind waves"
    u"U component of wind"
    u"V component of wind"
}

ww3_var_names_short = {
    u"wvdir",
    u"mpww",
    u"dirpw",
    u"perpw",
    u"dirsw",
    u"persw",
    u"swh",
    u"shww",
    u"u",
    u"v"
}

# Wavewatch III lat/lon grid


def ww3_grid():
    """
    Return the lat and lon grid locations
    for WW3 model.

    Uses `ww3_f` as input but this could be
    any WW3 output file
    """

    # Read file
    ww3 = pygrib.open(ww3_f)

    # Get gribmessage
    grb = ww3.read(1)[0]

    lat, lon = grb.latlons()

    return lat, lon


def ww3_mask(lat_range, lon_range, grb=None):
    """

    """
    # Read file
    ww3 = pygrib.open(ww3_f)

    # Get gribmessage
    if grb is None:
        grb = ww3.read(1)[0]

    # Get data
    data = grb.data(lat1=lat_range[0], lat2=lat_range[1],
                    lon1=lon_range[0], lon2=lon_range[1])

    # Return mask
    return data[0].mask
