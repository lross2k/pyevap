import openpyxl
from typing import TypedDict, Sequence
from collections import defaultdict
from datetime import datetime, time
from math import fsum

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

def main() -> None:
    data = load_data('test_data.xlsx')
    data = get_data_at(data, index_by_date(data['date'])[2019][12][1])
    print(values_for_variable(data['TA']))
    print(values_for_variable(data['HR']))
    print(values_for_variable(data['VV']))
    print(values_for_variable(data['RS']))
    print(values_for_variable(data['PR']))

if __name__ == "__main__":
    main()
