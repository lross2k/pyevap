import openpyxl
from typing import TypedDict
from collections import defaultdict
from datetime import datetime, time

class SoilData(TypedDict):
    date:   list[datetime]
    H:      list[time]
    TA:     list[str]
    HR:     list[int]
    VV:     list[str]
    RS:     list[int]
    PR:     list[str]

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

def load_data(file: str) -> SoilData:
    wb = openpyxl.load_workbook(file)
    ws = wb.active if 'Datos' not in wb.sheetnames else wb['Datos']
    spreadsheet_data: SoilData = {'date': [], 'H': [], 'TA': [], 'HR': [], 'VV': [], 'RS': [], 'PR': []}
    for row in list(ws.rows)[1:]:
        for index in range(len(spreadsheet_data.keys())):
            spreadsheet_data[list(spreadsheet_data.keys())[index]].append(row[index].value) # type: ignore
    return(spreadsheet_data)

def main() -> None:
    data = load_data('test_data.xlsx')
    data = get_data_at(data, index_by_date(data['date'])[2019][12][1])
    print(min(data['HR']))

if __name__ == "__main__":
    main()
