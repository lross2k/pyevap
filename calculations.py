from common import save_temp_to_system
from evapotranspiration import *
from math import pi

def append_with_separator(source: str, destination: str) -> str:
    transformed: str = destination
    transformed = transformed + ";" + source
    return transformed

def stringify_iteration(ta_values: dict[str, float], hr_values: dict[str, float],
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
                    year: int, month: int, day: int, amount_of_days: int) -> str:
    final_string: str = f'{month}/{day}/{year}'
    final_string = append_with_separator(str(amount_of_days), final_string)
    final_string = append_with_separator("%.3f" % (ta_values['avg']), final_string)
    final_string = append_with_separator("%.3f" % (hr_values['avg']), final_string)
    final_string = append_with_separator("%.3f" % (vv_values['avg']), final_string)
    final_string = append_with_separator("%.3f" % (rs_values['avg']), final_string)
    final_string = append_with_separator("%.3f" % (pr_values['avg']), final_string)
    final_string = append_with_separator("%.3f" % (ta_values['min']), final_string)
    final_string = append_with_separator("%.3f" % (hr_values['min']), final_string)
    final_string = append_with_separator("%.3f" % (vv_values['min']), final_string)
    final_string = append_with_separator("%.3f" % (rs_values['min']), final_string)
    final_string = append_with_separator("%.3f" % (pr_values['min']), final_string)
    final_string = append_with_separator("%.3f" % (ta_values['max']), final_string)
    final_string = append_with_separator("%.3f" % (hr_values['max']), final_string)
    final_string = append_with_separator("%.3f" % (vv_values['max']), final_string)
    final_string = append_with_separator("%.3f" % (rs_values['max']), final_string)
    final_string = append_with_separator("%.3f" % (pr_values['max']), final_string)
    final_string = append_with_separator("%.3f" % (wind_velocity), final_string)
    final_string = append_with_separator("%.3f" % (sat_steam['e_t_max']), final_string)
    final_string = append_with_separator("%.3f" % (sat_steam['e_t_min']), final_string)
    final_string = append_with_separator("%.3f" % (sat_steam['avg_p']), final_string)
    final_string = append_with_separator("%.3f" % (saturation_slope), final_string)
    final_string = append_with_separator("%.3f" % (p_real), final_string)
    final_string = append_with_separator("%.3f" % (steam_pressure_deficit), final_string)
    final_string = append_with_separator("%.3f" % (solar_radiation), final_string)
    final_string = append_with_separator("%.3f" % (julian_day), final_string)
    final_string = append_with_separator("%.3f" % (relative_distance), final_string)
    final_string = append_with_separator("%.3f" % (solar_declination), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['value_b']), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['seccional_correction']), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['sunset']), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['sun_middle_point']), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['start']), final_string)
    final_string = append_with_separator("%.3f" % (hourly_radicion_angle['end']), final_string)
    final_string = append_with_separator("%.3f" % (extraterrestrial_radiation), final_string)
    final_string = append_with_separator("%.3f" % (max_duration), final_string)
    final_string = append_with_separator("%.3f" % (r_so), final_string)
    final_string = append_with_separator("%.3f" % (radiations['short_wave']), final_string)
    final_string = append_with_separator("%.3f" % (radiations['relative']), final_string)
    final_string = append_with_separator("%.3f" % (radiations['long_wave']), final_string)
    final_string = append_with_separator("%.3f" % (radiations['net']), final_string)
    final_string = append_with_separator("%.3f" % (soil_heat_flux), final_string)
    final_string = append_with_separator("%.3f" % (evapotranspiration), final_string)
    return final_string

def deg_2_rad(degrees: float) -> float:
    return degrees*pi/180.0

def run_scenario(input_start_date: dict[str, str], input_end_date: dict[str, str], data: SoilData, constants: dict[str, float], interval: int = 0) -> bool:
    indexed_data = index_by_date(data['date'])

    start_date: dict[str, int] = {
        'year': data['date'][0].year if input_start_date['year'] == "" else int(input_start_date['year']),
        'month': data['date'][0].month if input_start_date['month'] == "" else int(input_start_date['month']),
        'day': data['date'][0].day if input_start_date['day'] == "" else int(input_start_date['day'])
    }

    end_date: dict[str, int] = {
        'year': data['date'][-1].year if input_end_date['year'] == "" else int(input_end_date['year']),
        'month': data['date'][-1].month if input_end_date['month'] == "" else int(input_end_date['month']),
        'day': data['date'][-1].day if input_end_date['day'] == "" else int(input_end_date['day'])
    }

    if len(data['date']) <= 0:
        print('No base data')
        return False

    if start_date['year'] < data['date'][0].year or start_date['month'] < data['date'][0].year or (start_date['day'] < data['date'][0].day if start_date['year'] == data['date'][0].year and start_date['month'] == data['date'][0].month else False):
        print('adjusting start date')
        start_date['year'] = data['date'][0].year
        start_date['month'] = data['date'][0].month
        start_date['day'] = data['date'][0].day

    if end_date['year'] > data['date'][-1].year or end_date['month'] > data['date'][-1].year or (end_date['day'] > data['date'][-1].day if end_date['year'] == data['date'][-1].year and end_date['month'] == data['date'][-1].month else False):
        print('adjusting end date')
        end_date['year'] = data['date'][-1].year
        end_date['month'] = data['date'][-1].month
        end_date['day'] = data['date'][-1].day

    print(start_date)
    print(end_date)

    csv_results: list[str] = []

    amount_of_days = 0
    prev_ta_avg: float = 0

    for year in range(start_date['year'], end_date['year'] + 1):
        for month in range(start_date['month'], end_date['month'] + 1):
            for day in range(start_date['day'], end_date['day'] + 1):
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

                csv_results.append(stringify_iteration(ta_values, hr_values, vv_values, rs_values, pr_values, wind_velocity, saturation_slope, sat_steam, p_real, steam_pressure_deficit, solar_radiation, julian_day, relative_distance, solar_declination, hourly_radicion_angle, extraterrestrial_radiation, max_duration, r_so, radiations, soil_heat_flux, evapotranspiration, year, month, day, amount_of_days))

                prev_ta_avg = ta_values['avg']

    save_temp_to_system(csv_results)
    return True
