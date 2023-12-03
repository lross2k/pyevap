from evapotranspiration import *

def print_iteration(ta_values: dict[str, float], hr_values: dict[str, float], 
                    vv_values: dict[str, float], rs_values: dict[str, float], 
                    pr_values: dict[str, float], wind_velocity: float, 
                    saturation_slope: float, sat_steam: dict[str, float], 
                    p_real: float, steam_pressure_deficit: float, 
                    solar_radiation: float, julian_day: float, 
                    relative_distance:float , solar_declination: float, 
                    hourly_radicion_angle: dict[str, float], 
                    extraterrestrial_radiation: float, max_duration: float, 
                    r_so: float, radiations: dict[str, float], 
                    soil_heat_flux: float, evapotranspiration: float,
                    year: int, month: int, day: int, amount_of_days: int) -> None:
    print("Iteration data starting")
    print(f'{month}/{day}/{year}')
    print(amount_of_days)
    print("%.3f %.3f %.3f %.3f %.3f" % (ta_values['avg'], hr_values['avg'], vv_values['avg'], rs_values['avg'], pr_values['avg']))
    print("%.3f %.3f %.3f %.3f %.3f" % (ta_values['min'], hr_values['min'], vv_values['min'], rs_values['min'], pr_values['min']))
    print("%.3f %.3f %.3f %.3f %.3f" % (ta_values['max'], hr_values['max'], vv_values['max'], rs_values['max'], pr_values['max']))
    print(wind_velocity)
    print("%.3f %.3f %.3f" % (sat_steam['e_t_max'], sat_steam['e_t_min'], sat_steam['avg_p']))
    print(saturation_slope)
    print(p_real)
    print(steam_pressure_deficit)
    print(solar_radiation)
    print(julian_day)
    print(relative_distance)
    print(solar_declination)
    print("%.3f %.3f %.3f %.3f %.3f %.3f" % (hourly_radicion_angle['value_b'], hourly_radicion_angle['seccional_correction'], hourly_radicion_angle['sunset'], hourly_radicion_angle['sun_middle_point'], hourly_radicion_angle['start'], hourly_radicion_angle['end']))
    print(extraterrestrial_radiation)
    print(max_duration)
    print(r_so)
    print("%.3f %.3f %.3f %.3f" % (radiations['short_wave'], radiations['relative'], radiations['long_wave'], radiations['net']))
    print(soil_heat_flux)
    print(evapotranspiration)
    print("Iteration data ending\n")

def example_iteration(constants: dict[str, float]) -> None:
    # Data obtained from file and processed
    data = load_data('test_data.xlsx')
    indexed_data = index_by_date(data['date'])

    # Values defined by the user
    # datetime_start
    # datetime_end
    # datetime_step

    # Values defined by iterative loop
    year = 2019
    month = 12
    day = 1

    # Iterative loop procedure
    data = get_data_at(data, indexed_data[year][month][day])
    prev_ta_avg = 0
    amount_of_days = 0

    amount_of_days += 1

    ta_values = values_for_variable(data['TA'])
    hr_values = values_for_variable(data['HR'])
    vv_values = values_for_variable(data['VV'])
    rs_values = values_for_variable(data['RS'])
    pr_values = values_for_variable(data['PR']) # Never used for calculations

    wind_velocity = calculate_wind_velocity(vv_values['avg'], constants)
    sat_steam = calculate_saturate_steam(ta_values['max'], ta_values['min'])
    saturation_slope = calculate_saturate_slope(ta_values['avg'])
    p_real = calculate_real_steam_pressure(ta_values['min'], ta_values['max'], hr_values['min'], hr_values['max'])
    steam_pressure_deficit = calculate_steam_pressure_deficit(sat_steam['avg_p'], p_real)
    solar_radiation = calculate_solar_radiation(rs_values['avg'])
    julian_day = calculate_julian_day(month, day)
    relative_distance = calculate_relative_distance(julian_day)
    solar_declination = calculate_solar_declination(julian_day)
    hourly_radicion_angle = calculate_hourly_radicion_angle(julian_day, solar_declination, constants)
    extraterrestrial_radiation = calculate_extraterrestrial_radiation(constants, relative_distance, solar_declination, hourly_radicion_angle['sunset'], hourly_radicion_angle['sun_middle_point'])
    max_duration = calculate_max_duration(hourly_radicion_angle['sunset']) # Never used for calculations
    r_so = calculate_r_so(constants, extraterrestrial_radiation) 
    radiations = calculate_radiations(constants, solar_radiation, r_so, ta_values['max'], ta_values['min'], p_real)
    soil_heat_flux = calculate_soil_heat_flux(constants, ta_values['avg'], prev_ta_avg, amount_of_days)
    evapotranspiration = calculate_evapotranspiration(saturation_slope, radiations['net'], soil_heat_flux, wind_velocity, ta_values['avg'], steam_pressure_deficit, constants)

    print_iteration(ta_values, hr_values, vv_values, rs_values, pr_values, wind_velocity, saturation_slope, sat_steam, p_real, steam_pressure_deficit, solar_radiation, julian_day, relative_distance, solar_declination, hourly_radicion_angle, extraterrestrial_radiation, max_duration, r_so, radiations, soil_heat_flux, evapotranspiration, year, month, day, amount_of_days)

def run_scenario(start_date: dict[str, int], end_date: dict[str, int], data: SoilData, constants: dict[str, float], interval: int = 0) -> None:
    indexed_data = index_by_date(data['date'])

    amount_of_days = 0
    prev_ta_avg = 0

    for year in range(start_date['year'], end_date['year'] + 1):
        for month in range(start_date['month'], end_date['month'] + 1):
            for day in range(start_date['day'], end_date['day'] + 1):
                print(f'{month}/{day}/{year}')

                amount_of_days += 1
                day_data = get_data_at(data, indexed_data[year][month][day])
                
                ta_values = values_for_variable(day_data['TA'])
                hr_values = values_for_variable(day_data['HR'])
                vv_values = values_for_variable(day_data['VV'])
                rs_values = values_for_variable(day_data['RS'])
                pr_values = values_for_variable(day_data['PR']) # Never used for calculations

                wind_velocity = calculate_wind_velocity(vv_values['avg'], constants)
                sat_steam = calculate_saturate_steam(ta_values['max'], ta_values['min'])
                saturation_slope = calculate_saturate_slope(ta_values['avg'])
                p_real = calculate_real_steam_pressure(ta_values['min'], ta_values['max'], hr_values['min'], hr_values['max'])
                steam_pressure_deficit = calculate_steam_pressure_deficit(sat_steam['avg_p'], p_real)
                solar_radiation = calculate_solar_radiation(rs_values['avg'])
                julian_day = calculate_julian_day(month, day)
                relative_distance = calculate_relative_distance(julian_day)
                solar_declination = calculate_solar_declination(julian_day)
                hourly_radicion_angle = calculate_hourly_radicion_angle(julian_day, solar_declination, constants)
                extraterrestrial_radiation = calculate_extraterrestrial_radiation(constants, relative_distance, solar_declination, hourly_radicion_angle['sunset'], hourly_radicion_angle['sun_middle_point'])
                max_duration = calculate_max_duration(hourly_radicion_angle['sunset']) # Never used for calculations
                r_so = calculate_r_so(constants, extraterrestrial_radiation) 
                radiations = calculate_radiations(constants, solar_radiation, r_so, ta_values['max'], ta_values['min'], p_real)
                soil_heat_flux = calculate_soil_heat_flux(constants, ta_values['avg'], prev_ta_avg, amount_of_days)
                evapotranspiration = calculate_evapotranspiration(saturation_slope, radiations['net'], soil_heat_flux, wind_velocity, ta_values['avg'], steam_pressure_deficit, constants)

                print_iteration(ta_values, hr_values, vv_values, rs_values, pr_values, wind_velocity, saturation_slope, sat_steam, p_real, steam_pressure_deficit, solar_radiation, julian_day, relative_distance, solar_declination, hourly_radicion_angle, extraterrestrial_radiation, max_duration, r_so, radiations, soil_heat_flux, evapotranspiration, year, month, day, amount_of_days)

                prev_ta_avg = ta_values['avg']

def main() -> None:
    constants = {
        'measure_height_c': 6.5,
        'latitude_rad_c': 0.173,
        'max_point_c': 12,
        'centre_logitude_deg_c': 90,
        'longitude_deg_c': 83.9,
        'solar_c': 0.082,
        'height_c': 2129,
        'albedo_c': 0.23,
        'steffan_c': (4.903*10**(-9))/24,
        'caloric_capacity_c': 2.1,
        'soil_depth_c': 0.1,
        'psicrometric_c': 0.05
    }

    start_date = {
        'month': 12,
        'day': 1,
        'year': 2019
    }

    end_date = {
        'month': 12,
        'day': 3,
        'year': 2019
    }

    data = load_data('test_data.xlsx')

    run_scenario(start_date, end_date, data, constants)

if __name__ == "__main__":
    main()
