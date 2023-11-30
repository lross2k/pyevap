import openpyxl
from collections import defaultdict
from datetime import datetime

def index_by_date(data: list[datetime]) -> defaultdict[int, defaultdict[int, defaultdict[int, list[int]]]]:
    ''' Turn a list of datetime values into dict of dicts callable as 
            [year: int][month: int][day: int] 
        which returns a list with all the indexes of the original list 
        which correspond to said date '''
    index_date: defaultdict[int, defaultdict[int, defaultdict[int, list[int]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for index in range(len(data)):
        index_date[data[index].year][data[index].month][data[index].day].append(index)
    return(index_date)

def load_data():
    file = 'test_data.xlsx'
    wb = openpyxl.load_workbook(file)
    ws = wb.active if 'Datos' not in wb.sheetnames else wb['Datos']
    spreadsheet_data: dict[str, list[datetime]] = {}
    for col in ws['A1:G1'][0]:
        spreadsheet_data[col.value] = []
    for row in list(ws.rows)[1:]:
        for index in range(len(spreadsheet_data.keys())):
            spreadsheet_data[list(spreadsheet_data.keys())[index]].append(row[index].value)
    return(spreadsheet_data)

def main() -> None:
    data = load_data()
    print(index_by_date(data['date'])[2019][12][2])

if __name__ == "__main__":
    main()
