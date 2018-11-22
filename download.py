import cdsapi
import os

months = [
    ['07', '08'],
    ['09', '10']
    ['11', '12'],
]

years = ['2017']

for y in years:
    for m in months:

        f_out = '{}_{}_{}.grib'.format(y, m[0], m[1])

        if not os.path.exists(f_out):
            c = cdsapi.Client()

            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'format': 'grib',
                    'variable': [
                        'air_density_over_the_oceans', 'altimeter_corrected_wave_height', 'altimeter_wave_height',
                        'coefficient_of_drag_with_waves', 'free_convective_velocity_over_the_oceans', 'maximum_individual_wave_height',
                        'mean_direction_of_total_swell', 'mean_direction_of_wind_waves', 'mean_period_of_total_swell',
                        'mean_period_of_wind_waves', 'mean_square_slope_of_waves', 'mean_wave_direction',
                        'mean_wave_direction_of_first_swell_partition', 'mean_wave_direction_of_second_swell_partition', 'mean_wave_direction_of_third_swell_partition',
                        'mean_wave_period', 'mean_wave_period_based_on_first_moment', 'mean_wave_period_based_on_first_moment_for_swell',
                        'mean_wave_period_based_on_first_moment_for_wind_waves', 'mean_wave_period_based_on_second_moment_for_swell', 'mean_wave_period_based_on_second_moment_for_wind_waves',
                        'mean_wave_period_of_first_swell_partition', 'mean_wave_period_of_second_swell_partition', 'mean_wave_period_of_third_swell_partition',
                        'mean_zero_crossing_wave_period', 'normalized_energy_flux_into_ocean', 'normalized_energy_flux_into_waves',
                        'normalized_stress_into_ocean', 'peak_wave_period', 'period_corresponding_to_maximum_individual_wave_height',
                        'significant_height_of_combined_wind_waves_and_swell', 'significant_height_of_total_swell', 'significant_height_of_wind_waves',
                        'significant_wave_height_of_first_swell_partition', 'significant_wave_height_of_second_swell_partition', 'significant_wave_height_of_third_swell_partition',
                        'wave_spectral_directional_width', 'wave_spectral_directional_width_for_swell', 'wave_spectral_directional_width_for_wind_waves',
                        'wave_spectral_kurtosis', 'wave_spectral_peakedness', 'wave_spectral_skewness'
                    ],
                    'year': '2017',
                    'month': [
                        '01', '02', '03'
                    ],
                    'day': [
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
                    ]
                },
                f_out)
