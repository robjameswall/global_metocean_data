"""
Download ECMWF ERA5 reanalysis data
"""

import os
import cdsapi
import itertools

# Set day range in to first and second half of month
days = [
    '01', '02', '03',
    '04', '05', '06',
    '07', '08', '09',
    '10', '11', '12',
    '13', '14', '15',
    '16', '17', '18',
    '19', '20', '21',
    '22', '23', '24',
    '25', '26', '27',
    '28', '29', '30',
    '31'
]

# Set variables to download
variables = [
    '10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_direction_of_total_swell',
    'mean_direction_of_wind_waves', 'mean_period_of_total_swell', 'mean_period_of_wind_waves',
    'mean_wave_direction', 'mean_wave_direction_of_first_swell_partition', 'mean_wave_direction_of_second_swell_partition',
    'mean_wave_period', 'mean_wave_period_based_on_first_moment_for_swell', 'mean_wave_period_of_first_swell_partition',
    'mean_wave_period_of_second_swell_partition', 'significant_height_of_combined_wind_waves_and_swell', 'significant_height_of_wind_waves'
]


def get_month_str(n):
    """
    Zero pad month if necessary
    n : integer, will pad zeros if below 10
    """

    return str(n).rjust(2, "0")


def get_filename(month, year):
    """
    Create output filename

    month: int
    year: int
    """

    year = str(year)
    month = get_month_str(month)

    out_f = "era5_{}{}.grib".format(year, month)

    return out_f


def year_month_combos(year, month_start, month_end):
    """
    Create tuples of year and month combos
    """
    month_range = list(range(month_start, month_end + 1))
    combined = [c for c in itertools.product([year], month_range)]

    return combined


def all_year_month_combos(latest_year=2018, latest_month=9,
                          start_year=2017, start_month=6):
    """
    Return list with a tuple (year, month) of combinations from
    start month
    """

    fp_list = []
    for year in range(start_year, latest_year + 1):
        if year == start_year:
            yr_combo = year_month_combos(year, start_month, 12)
            fp_list.append(yr_combo)
        elif year == latest_year:
            yr_combo = year_month_combos(year, 1, latest_month)
            fp_list.append(yr_combo)
        else:
            yr_combo = year_month_combos(year, 1, 12)
            fp_list.append(yr_combo)

    all_combos = sum(fp_list, [])

    return all_combos


def get_all_filenames(latest_year=2018, latest_month=11, directory=None,
                      start_year=2017, start_month=6):
    """
    Get all output filenames
    """

    all_combos = all_year_month_combos(
        latest_year=latest_year, latest_month=latest_month,
        start_year=start_year, start_month=start_month)
    all_filepaths = [get_filename(r[1], r[0]) for r in all_combos]

    if directory is not None:
        all_filepaths = [os.path.join(directory, fn) for fn in all_filepaths]
    return all_filepaths


def download_era5(month, year, variables=variables,
                  directory=None, overwrite=False, fn=None):
    """
    Download reanalysis ERA5 data

        month: int,
        year: int
        variables: list, variables to download,
        directory: str, directory path to output to
        overwrite: boolean, overwrite existing output
        fn: str [optional], output filename
    """

    # Create api client
    c = cdsapi.Client()

    # Output file path
    if fn is None:
        fn = get_filename(month, year)

    if directory is not None:
        fn = os.path.join(directory, fn)

    # Get data
    if not os.path.exists(fn) or overwrite:
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'variable': variables,
                'product_type': 'reanalysis',
                'year': str(year),
                'day': days,
                'month': get_month_str(month),
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00'
                ],
                'format': 'grib'
            },
            fn)


def download_range(year_start=2017, month_start=6,
                   latest_year=2018, latest_month=11, directory="data"):
    """

    """

    # Get all output filenames within this range
    all_fns = get_all_filenames(latest_year=latest_year, latest_month=latest_month,
                                start_year=year_start, start_month=month_start,
                                directory=directory)

    # Check if
    all_downloaded = all([os.path.exists(fn) for fn in all_fns])

    while not all_downloaded:
        # Loop through files and download if doesn't exist
        for fn in all_fns:
            # Check if exits
            if not os.path.exists(fn):
                # Get year and month from filename
                year = int(fn[-11:-7])
                month = int(fn[-7:-5])

                try:
                    print("Downloading: {}".format(fn))
                    # Download file
                    download_era5(month=month, year=year, directory=directory)
                except:
                    print("Failed to download {}".format(fn))

            # Update download check
            all_downloaded = all([os.path.exists(fn) for fn in all_fns])


if __name__ == "__main__":
    download_range()
