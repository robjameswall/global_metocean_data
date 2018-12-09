import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_direction_of_total_swell',
            'mean_direction_of_wind_waves', 'mean_period_of_total_swell', 'mean_period_of_wind_waves',
            'mean_wave_direction', 'mean_wave_direction_of_first_swell_partition', 'mean_wave_direction_of_second_swell_partition',
            'mean_wave_period', 'mean_wave_period_based_on_first_moment_for_swell', 'mean_wave_period_of_first_swell_partition',
            'mean_wave_period_of_second_swell_partition', 'significant_height_of_combined_wind_waves_and_swell', 'significant_height_of_wind_waves'
        ],
        'product_type': 'reanalysis',
        'year': '2018',
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12'
        ],
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
    'data/era5_20180601_full.grib')
