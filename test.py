import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'grib',
        'variable':[
            '10m_u_component_of_wind','10m_v_component_of_wind','2m_dewpoint_temperature',
            '2m_temperature','mean_sea_level_pressure','mean_wave_direction',
            'mean_wave_direction_of_first_swell_partition','mean_wave_direction_of_second_swell_partition','mean_wave_direction_of_third_swell_partition',
            'mean_wave_period','mean_wave_period_of_second_swell_partition','mean_wave_period_of_third_swell_partition',
            'peak_wave_period','sea_surface_temperature','significant_height_of_combined_wind_waves_and_swell',
            'significant_wave_height_of_first_swell_partition','significant_wave_height_of_second_swell_partition','significant_wave_height_of_third_swell_partition',
            'surface_pressure','total_precipitation'
        ],
        'year':'2017',
        'month':'06',
        'day':[
            '01','02','03'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ]
    },
    'download.grib')