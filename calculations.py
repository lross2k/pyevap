import openpyxl
from typing import TypedDict, Sequence
from collections import defaultdict
from datetime import datetime, time
from math import fsum, log, exp, cos, pi, sin, acos, tan, sqrt

class SoilData(TypedDict):
    date:   list[datetime]
    H:      list[time]
    TA:     list[float]
    HR:     list[int]
    VV:     list[float]
    RS:     list[int]
    PR:     list[float]

def index_by_date(data: list[datetime]) -> defaultdict[int, defaultdict[int, defaultdict[int, list[int]]]]:
    ''' Turn a list of datetime values into dict of dicts callable as 
            [year: int][month: int][day: int] 
        which returns a list with all the indexes of the original list 
        which correspond to said date '''
    index_date: defaultdict[int, defaultdict[int, defaultdict[int, list[int]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for index in range(len(data)):
        index_date[data[index].year][data[index].month][data[index].day].append(index)
    return(index_date)

def get_data_at(data: SoilData, indexes: list[int]) -> SoilData:
    new_data: SoilData = {'date': [], 'H': [], 'TA': [], 'HR': [], 'VV': [], 'RS': [], 'PR': []}
    for index in indexes:
        new_data['date'].append(data['date'][index])
        new_data['H'].append(data['H'][index])
        new_data['TA'].append(data['TA'][index])
        new_data['HR'].append(data['HR'][index])
        new_data['VV'].append(data['VV'][index])
        new_data['RS'].append(data['RS'][index])
        new_data['PR'].append(data['PR'][index])
    return(new_data)

def values_for_variable(variable_data: Sequence[float]) -> dict[str, float]:
    values = {'avg': fsum(variable_data) / len(variable_data),
        'min': min(variable_data),
        'max': max(variable_data)}
    return(values)

def load_data(file: str) -> SoilData:
    wb = openpyxl.load_workbook(file)
    ws = wb.active if 'Datos' not in wb.sheetnames else wb['Datos']
    spreadsheet_data: SoilData = {'date': [], 'H': [], 'TA': [], 'HR': [], 'VV': [], 'RS': [], 'PR': []}
    for row in list(ws.rows)[1:]:
        spreadsheet_data['date'].append(row[0].value)
        spreadsheet_data['H'].append(row[1].value)
        spreadsheet_data['TA'].append(float(row[2].value))
        spreadsheet_data['HR'].append(row[3].value)
        spreadsheet_data['VV'].append(float(row[4].value))
        spreadsheet_data['RS'].append(row[5].value)
        spreadsheet_data['PR'].append(float(row[6].value))
    return(spreadsheet_data)

def calculate_wind_velocity(vv_avg: float, measure_height_c: float) -> float:
    """ Equation 47 speed of wind at 2m u_2 (m/2) """
    velocity = vv_avg*(4.87/(log((67.8*measure_height_c)-5.42)))
    return velocity

def calculate_saturate_steam(ta_max: float, ta_min: float) -> dict[str, float]:
    """ Equations 12 and 18 e(Tmax) e(Tmin) avg pressure in kPa """
    e_t_max = 0.6108*exp((17.27*ta_max)/(ta_max+237.3))
    e_t_min = 0.6108*exp((17.27*ta_min)/(ta_min+237.3))
    avg_p = (e_t_max + e_t_min)/2.0
    return {'e_t_max': e_t_max, 'e_t_min': e_t_min, 'avg_p': avg_p}

def calculate_saturate_slope(ta_avg: float) -> float:
    """ Equation 13 Δ (kPa/ C°1) """
    slope = (4098*(0.6108*exp((17.27*ta_avg)/(ta_avg+237.3))))/(ta_avg+237.3)**2
    return slope

def calculate_real_steam_pressure(ta_min: float, ta_max: float, hr_min: float, hr_max: float) -> float:
    """ Equation 17 kPa """
    first_factor = (0.6108*exp((17.27*ta_min)/(ta_min+237.3)))*(hr_max/100)
    second_factor = (0.6108*exp((17.27*ta_max)/(ta_max+237.3)))*(hr_min/100)
    real_pressure = (first_factor + second_factor)/2.0
    return real_pressure

def calculate_steam_pressure_deficit(avg_pressure: float, real_pressure: float) -> float:
    """ kPa """
    pressure_deficit = avg_pressure - real_pressure
    return pressure_deficit

def calculate_solar_radiation(rs_avg: float) -> float:
    """ MJ/m^(2)* """
    solar_radiation = rs_avg * 0.0864
    return solar_radiation

def calculate_julian_day(month: int, day: int) -> float:
    julian_day = ((275*(month/9))-30+day)-2
    return julian_day

def calculate_relative_distance(julian_day: float) -> float:
    """ Equation 23 """
    relative_distance = 1+(0.033*cos((2*pi*julian_day/365)))
    return relative_distance

def calculate_solar_declination(julian_day: float) -> float:
    """ Equation 24 δ """
    solar_declination = 0.409*(sin((((2*pi)*(julian_day/365))-1.39)))
    return solar_declination

def calculate_hourly_radicion_angle(julian_day: float, solar_declination: float, latitude_rad_c: float, max_point_c: float,
                                    centre_logitude_deg_c: float, longitude_deg_c: float) -> dict[str, float]:
    """ Equations 33, 32, 25, 31 with median point from 12, 29 and 30 """
    value_b = (2*pi*(julian_day-81))/364
    seccional_correction = (0.1645*sin(2*value_b))-(0.1255*cos(value_b))-(0.025*sin(value_b))
    sunset = acos(-tan(latitude_rad_c)*tan(solar_declination))
    sun_middle_point = (pi/12)*((max_point_c+0.06667*(centre_logitude_deg_c-longitude_deg_c)+seccional_correction)-12)
    start = sun_middle_point-(pi/24)
    end = sun_middle_point+(pi/24)
    return {'value_b': value_b, 'seccional_correction': seccional_correction, 'sunset': sunset,
            'sun_middle_point': sun_middle_point, 'start': start, 'end': end}

def calculate_extraterrestrial_radiation(solar_c: float, latitude_rad_c: float, relative_distance: float, solar_declination: float, sunset: float, sun_middle_point: float) -> float:
    """ Equation 21 MJ/m^2 """
    ra = ((24*60)/pi)*(solar_c*relative_distance)*((sunset*sin(latitude_rad_c)*sin(solar_declination))+(cos(latitude_rad_c)*cos(solar_declination)*sin(sun_middle_point)))
    return ra

def calculate_max_duration(sunset: float) -> float:
    """ Equation 34 """
    max_duration = (24/pi)*sunset
    return max_duration

def calculate_r_so(height_c: float, extraterrestrial_radiation: float) -> float:
    """ Equation 37 MJ/ m^(2)* """
    r_so = (0.75+2*10**(-5)*height_c)*extraterrestrial_radiation
    return r_so

def calculate_radiations(albedo_c: float, steffan_c: float, solar_radiation: float, r_so: float, 
                        ta_max: float, ta_min: float, p_real: float) -> dict[str, float]:
    """ Equations 38, 39 and 40 """
    short_wave_radiation = (1-albedo_c)*solar_radiation # MJ/ m^(2)*
    relative_radiation = solar_radiation/r_so
    long_wave_radiation = steffan_c*(((ta_max+273.16)+(ta_min+273.16))/2)*(0.34-0.14*sqrt(p_real))*((1.35*relative_radiation)-0.35) # MJ/ m^(2)*
    net_radiation = short_wave_radiation - long_wave_radiation # MJ/ m^(2)*
    return {'short_wave': short_wave_radiation, 'relative': relative_radiation, 'long_wave': long_wave_radiation, 'net': net_radiation}

def calculate_soil_heat_flux(caloric_capacity_c: float, soil_depth_c: float, ta_avg: float, prev_ta_avg: float, amount_of_days: int) -> float:
    """ Equations 45 and 46 MJ/ m^(2)* """
    heat_flux = caloric_capacity_c*((ta_avg-prev_ta_avg)/(amount_of_days))*soil_depth_c
    return heat_flux

def calculate_evapotranspiration(saturation_slope: float, net_radiation: float, soil_heat_flux: float, 
                                wind_velocity: float, ta_avg: float, steam_pressure_deficit: float, 
                                psicrometric_c: float) -> float:
    numerator_1 = 0.408*saturation_slope*(net_radiation-soil_heat_flux)
    numerator_2 = psicrometric_c*(900/(ta_avg+273))*wind_velocity*(steam_pressure_deficit)
    denominator = saturation_slope+(psicrometric_c*(1+0.34*wind_velocity))
    evapotranspiration = (numerator_1+numerator_2)/denominator
    return evapotranspiration

def main() -> None:
    # Data obtained from file and processed
    data = load_data('test_data.xlsx')
    indexed_data = index_by_date(data['date'])

    # Values defined by the user
    # datetime_start
    # datetime_end
    # datetime_step
    measure_height_c = 6.5
    latitude_rad_c = 0.173
    max_point_c = 12
    centre_logitude_deg_c = 90
    longitude_deg_c = 83.9
    solar_c = 0.082
    height_c = 2129
    albedo_c = 0.23
    steffan_c = (4.903*10**(-9))/24
    caloric_capacity_c = 2.1
    soil_depth_c = 0.1
    psicrometric_c = 0.05

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

    wind_velocity = calculate_wind_velocity(vv_values['avg'], measure_height_c)
    sat_steam = calculate_saturate_steam(ta_values['max'], ta_values['min'])
    saturation_slope = calculate_saturate_slope(ta_values['avg'])
    p_real = calculate_real_steam_pressure(ta_values['min'], ta_values['max'], hr_values['min'], hr_values['max'])
    steam_pressure_deficit = calculate_steam_pressure_deficit(sat_steam['avg_p'], p_real)
    solar_radiation = calculate_solar_radiation(rs_values['avg'])
    julian_day = calculate_julian_day(month, day)
    relative_distance = calculate_relative_distance(julian_day)
    solar_declination = calculate_solar_declination(julian_day)
    hourly_radicion_angle = calculate_hourly_radicion_angle(julian_day, solar_declination, latitude_rad_c, max_point_c, centre_logitude_deg_c, longitude_deg_c)
    extraterrestrial_radiation = calculate_extraterrestrial_radiation(solar_c, latitude_rad_c, relative_distance, solar_declination, hourly_radicion_angle['sunset'], hourly_radicion_angle['sun_middle_point'])
    r_so = calculate_r_so(height_c, extraterrestrial_radiation) 
    radiations = calculate_radiations(albedo_c, steffan_c, solar_radiation, r_so, ta_values['max'], ta_values['min'], p_real)
    soil_heat_flux = calculate_soil_heat_flux(caloric_capacity_c, soil_depth_c, ta_values['avg'], prev_ta_avg, amount_of_days)
    evapotranspiration = calculate_evapotranspiration(saturation_slope, radiations['net'], soil_heat_flux, wind_velocity, ta_values['avg'], steam_pressure_deficit, psicrometric_c)

    print(ta_values)
    print(hr_values)
    print(vv_values)
    print(rs_values)

    print(values_for_variable(data['PR'])) # Never used for calculations

    print(wind_velocity)
    print(saturation_slope)
    print(sat_steam)
    print(p_real)
    print(steam_pressure_deficit)
    print(solar_radiation)
    print(julian_day)
    print(relative_distance)
    print(solar_declination)
    print(hourly_radicion_angle)
    print(extraterrestrial_radiation)

    print(calculate_max_duration(hourly_radicion_angle['sunset'])) # Never used for calculations

    print(r_so)
    print(radiations)
    print(soil_heat_flux)
    print(evapotranspiration)

if __name__ == "__main__":
    main()
