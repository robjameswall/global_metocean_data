import processing as proc
import reanalysis as re
import os

site = "gold_coast"
fn = re.get_filename(directory="data")
out_dir = "out/linear"

for f in fn:
    if "201707" not in f:
        out_f = os.path.split(f)[1]
        out_f = out_f.replace(".grib", ".csv")
        out_f.replace("era5", site)
        out_full = os.path.join(out_dir, out_f)

        print("Loading {}".format(out_f))
        era = proc.Era5(grb_file=f, site="gold_coast")
        print("Formatting {}".format(out_f))
        era.format(method="linear")
        print("Saving {}".format(out_f))
        era.create_df()
        era.df.to_csv(out_f)
