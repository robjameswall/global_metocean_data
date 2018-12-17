"""Test Era5 class from processing.py
"""

import processing as proc
import utils
import os
import datetime

multi = True
if multi:
    nww3_f = [os.path.join("data", f) for f in os.listdir("data") if ("nww3" in f) and ("multi" in f)]
else:
    nww3_f = [os.path.join("data", f) for f in os.listdir("data") if ("nww3" in f) and ("multi" not in f)]

today_date_str = datetime.datetime.now().strftime("%Y%m%d")

# Load class
all_ww3 = []
for f in nww3_f:
    ww3 = proc.Ww3(f, site="gold_coast")
    ww3.format()
    ww3.create_df()
    out_str = "out/ww3/gold_coast_{}_".format(today_date_str)
    out_f = ww3.fn.replace("data/", out_str)
    out_f = out_f.replace(".grib.grib2.grb", ".csv")
    ww3.df.to_csv(out_f)

