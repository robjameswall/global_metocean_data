"""Test Era5 class from processing.py
"""

import processing as proc
import utils

# Load class
small_grb_f = "data/era5_201707.grib"
era = proc.Era5(small_grb_f, site='gold_coast')
era.format()