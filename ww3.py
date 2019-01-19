"""
Process ww3 forecasts to model input
"""

import processing as proc
import os


def process_ww3(site_name, in_grb, save=True, out_dir=None):
    """
    Process a ww3 forecast read for input to forecast models
    """

    # Read grb file
    g = proc.Ww3(in_grb, site=site_name)

    # Process and create dataframe
    g.format()
    g.create_df()

    # Save if true
    if save:
        grb_name = os.path.split(g.fn)[-1]
        anal_date = g.anal_date.strftime("%Y%m%d_%H%M")
        out_name = "{}_{}_{}".format(g.site, anal_date, grb_name)
        out_name = out_name.replace(".grib.grib2.grb", ".csv")
        out_full = os.path.join(out_dir, out_name)
        g.df.to_csv(out_full)

    return(g)
