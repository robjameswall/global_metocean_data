"""Test Era5 class from processing.py
"""

import processing as proc
import utils
import os

nww3_f = [os.path.join("data", f) for f in os.listdir("data") if "nww3" in f]

# Load class
all_ww3 = []
for f in nww3_f:
    ww3 = proc.Ww3(f, site="gold_coast")
    ww3.format()
    
    all_ww3.append(ww3)