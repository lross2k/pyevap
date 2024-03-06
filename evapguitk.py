from evapotranspiration import load_data, SoilData, calculate_decimal_degrees
from common import save_result_to_system, get_cache_file_path
from calculations import run_scenario, deg_2_rad
from tkinter import StringVar, filedialog
from typing import Callable, Any
import tkinter as tk
import openpyxl
import csv

class ScrolledCanvas():
    def __init__(self, root: tk.Frame) -> None:
        canv = tk.Canvas(root, relief=tk.SUNKEN)
        canv.config(width=800, height=500)

        canv.config(scrollregion=(0,0,5400, 500))
        canv.config(highlightthickness=0)

        xbar = tk.Scrollbar(root, orient='horizontal')
        xbar.config(command=canv.xview)
        canv.config(xscrollcommand=xbar.set)
        xbar.pack(side=tk.BOTTOM, fill=tk.X)
        canv.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.canv = canv

    def get_canv(self) -> tk.Canvas:
        return self.canv

class EvapTk:
    def __init__(self) -> None:
        self.TKroot = tk.Tk()
        self.TKroot.geometry("800x600")
        self.TKroot.title('PyEvap')

        self.dummy_sv: StringVar                = StringVar(value="")
        self.height_sv: StringVar               = StringVar(value="2129")
        self.albedo_sv: StringVar               = StringVar(value="0.23")
        self.solar_sv: StringVar                = StringVar(value="0.082")
        self.meassure_height_sv: StringVar      = StringVar(value="6.5")
        self.pressure_sv: StringVar             = StringVar(value="78.4")
        self.psicrometric_sv: StringVar         = StringVar(value="0.05")
        self.soil_depth_sv: StringVar           = StringVar(value="0.1")
        self.caloric_capacity_sv: StringVar     = StringVar(value="2.1")
        self.highest_point_sv: StringVar        = StringVar(value="12")
        self.lat_degrees_sv: StringVar          = StringVar(value="9")
        self.lat_min_sv: StringVar              = StringVar(value="55")
        self.lat_seconds_sv: StringVar          = StringVar(value="26")
        self.lat_decimals_sv: StringVar         = StringVar(value=str(calculate_decimal_degrees(int(self.lat_degrees_sv.get()), int(self.lat_min_sv.get()), int(self.lat_seconds_sv.get()))))
        self.lat_rads_sv: StringVar             = StringVar(value=str(deg_2_rad(float(self.lat_decimals_sv.get()))))
        self.long_degrees_sv: StringVar         = StringVar(value="83")
        self.long_min_sv: StringVar             = StringVar(value="53")
        self.long_seconds_sv: StringVar         = StringVar(value="48")
        self.long_decimals_sv: StringVar        = StringVar(value=str(calculate_decimal_degrees(int(self.long_degrees_sv.get()), int(self.long_min_sv.get()), int(self.long_seconds_sv.get()))))
        self.long_rads_sv: StringVar            = StringVar(value=str(deg_2_rad(float(self.long_decimals_sv.get()))))
        self.center_long_decimals_sv: StringVar = StringVar(value="90")
        self.center_long_rads_sv: StringVar     = StringVar(value=str(deg_2_rad(float(self.center_long_decimals_sv.get()))))
        self.start_date_year_sv: StringVar      = StringVar(value="2019")
        self.start_date_month_sv: StringVar     = StringVar(value="12")
        self.start_date_day_sv: StringVar       = StringVar(value="1")
        self.end_date_year_sv: StringVar        = StringVar(value="2019")
        self.end_date_month_sv: StringVar       = StringVar(value="12")
        self.end_date_day_sv: StringVar         = StringVar(value="3")

        self.input_frame = self.gen_input_frame()
        self.main_frame, self.result_frame = self.gen_main_frame()
        self.main_frame.pack()
        self.spreadsheet_data: SoilData = {'date': [], 'H': [], 'TA': [], 'HR': [], 'VV': [], 'RS': [], 'PR': []}

    def run(self) -> None:
        self.raise_input_menu()
        self.TKroot.mainloop()

    def gen_input_frame(self) -> tk.Frame:
        # Input frame basis
        input_frame = tk.Frame(self.TKroot)

        # Values that must be entered by the user
        #tk.Label(input_frame, text='Input Page').grid(row=2, column=0, columnspan=2)
        left_localization_data = tk.Frame(input_frame)
        self.new_input_row(left_localization_data, 1, 'Altura', 'msnm', self.height_sv, callback=self.height_callback)
        self.new_input_row(left_localization_data, 2, 'Albedo', '-', self.albedo_sv)
        self.new_input_row(left_localization_data, 3, 'Constante Solar', 'MJ/m^2 min', self.solar_sv)
        self.new_input_row(left_localization_data, 4, 'Altura de medición', 'm', self.meassure_height_sv)
        left_localization_data.grid(row=1, column=0, sticky='nswe')

        right_localization_data = tk.Frame(input_frame)
        self.new_input_row(right_localization_data, 1, 't=punto máximo', '-', self.highest_point_sv)
        self.new_input_row(right_localization_data, 2, 'Capacidad calorífica', 'MJ m-3 °C-1', self.caloric_capacity_sv)
        self.new_input_row(right_localization_data, 3, 'Δz=profundida del suelo', 'm', self.soil_depth_sv)
        right_localization_data.grid(row=1, column=1, sticky='nswe')

        # Values defined from other values
        tk.Label(input_frame, text='Valores calculados').grid(row=2, column=0, columnspan=1, sticky='w')

        calculated_data = tk.Frame(input_frame)
        self.new_input_row(calculated_data, 0, 'Presión Atmosférica', 'kPa', self.pressure_sv, disabled=True)
        self.new_input_row(calculated_data, 1, 'Constante psicrométrica (ϒ)', 'kPa /°C', self.psicrometric_sv, disabled=True)
        calculated_data.grid(row=3, column=0, sticky='nswe')

        # Values related to location
        tk.Label(input_frame, text='Ubicación').grid(row=4, column=0, columnspan=1)
        location_data = tk.Frame(input_frame, width=800, height=150)
        tk.Label(location_data, text='Grados',            padx=10, pady=10).grid(row=0, column=1)
        tk.Label(location_data, text='Minutos',           padx=10, pady=10).grid(row=0, column=2)
        tk.Label(location_data, text='Segundos',          padx=10, pady=10).grid(row=0, column=3)
        tk.Label(location_data, text='Grados decimales',  padx=0, pady=10).grid(row=0, column=4)
        tk.Label(location_data, text='Radianes',          padx=10, pady=10).grid(row=0, column=5)

        self.new_location_input_row(location_data, 1, 'Latitud (φ)', self.lat_degrees_sv, self.lat_min_sv, self.lat_seconds_sv,
                                    self.lat_decimals_sv, self.lat_rads_sv, self.location_lat_callback, False, False, False,
                                    True, True)
        self.new_location_input_row(location_data, 2, 'Longitud (Lm)', self.long_degrees_sv, self.long_min_sv, self.long_seconds_sv,
                                    self.long_decimals_sv, self.long_rads_sv, self.location_long_callback, False, False, False,
                                    True, True)
        self.new_location_input_row(location_data, 3, 'Longitud centro (Lz)', self.dummy_sv, self.dummy_sv, self.dummy_sv,
                                    self.center_long_decimals_sv, self.center_long_rads_sv,
                                    self.center_long_callback, True, True, True,
                                    False, True)
        location_data.grid(row=5, column=0, columnspan=2, sticky='nswe')

        # Date data frame
        date_data = tk.Frame(input_frame)
        tk.Label(date_data, text="Día", padx=10, pady=10).grid(row=0, column=1)
        tk.Label(date_data, text="Mes", padx=10, pady=10).grid(row=0, column=2)
        tk.Label(date_data, text="Año", padx=10, pady=10).grid(row=0, column=3)
        tk.Label(date_data, text="Inicio", padx=10, pady=10).grid(row=1, column=0)
        tk.Entry(date_data, textvariable=self.start_date_day_sv, width=15).grid(row=1, column=1, columnspan=1)
        tk.Entry(date_data, textvariable=self.start_date_month_sv, width=15).grid(row=1, column=2, columnspan=1)
        tk.Entry(date_data, textvariable=self.start_date_year_sv, width=15).grid(row=1, column=3, columnspan=1)
        tk.Label(date_data, text="Fin", padx=10, pady=10).grid(row=2, column=0)
        tk.Entry(date_data, textvariable=self.end_date_day_sv, width=15).grid(row=2, column=1, columnspan=1)
        tk.Entry(date_data, textvariable=self.end_date_month_sv, width=15).grid(row=2, column=2, columnspan=1)
        tk.Entry(date_data, textvariable=self.end_date_year_sv, width=15).grid(row=2, column=3, columnspan=1)
        date_data.grid(row=3, column=1, sticky='nswe')

        tk.Button(input_frame, text='Ir a calculos', command=self.raise_result_menu).grid(row=6, column=0, sticky='nswe')
        tk.Button(input_frame, text='Guardar resultados', command=self.save_results).grid(row=6, column=1, sticky='nswe')

        return input_frame

    def gen_main_frame(self) -> tuple[tk.Frame, tk.Canvas]:
        main_frame = tk.Frame(self.TKroot)
        #tk.Label(main_frame, text='Main Page').grid(row=0, column=0)
        tk.Button(main_frame, text='Cambiar parametros', command=self.raise_input_menu).pack()
        #main_frame.rowconfigure(0, weight=1)
        #main_frame.rowconfigure(1, weight=1)
        #main_frame.columnconfigure(0, weight=1)
        tk.Button(main_frame, text='Seleccionar datos', command=self.get_test_data).pack()
        tk.Button(main_frame, text='Calcular', command=self.run_scenario_example).pack()
        # used to be scrollable
        #result_frame = tk.ScrollableFrame(main_frame, width=800, height=500, orientation='horizontal')
        #result_frame = tk.Frame(main_frame, width=800, height=500)
        budget_scroll_frame = ScrolledCanvas(main_frame)
        result_frame = budget_scroll_frame.get_canv()
        #result_frame.grid(row=2, column=0, columnspan=3)
        return main_frame, result_frame

    def run_scenario_example(self) -> None:
        constants = {
            'measure_height_c': float(self.meassure_height_sv.get()),
            'latitude_rad_c': float(self.lat_rads_sv.get()),
            'max_point_c': int(self.highest_point_sv.get()),
            'centre_logitude_deg_c': float(self.center_long_decimals_sv.get()),
            'longitude_deg_c': float(self.long_decimals_sv.get()),
            'solar_c': float(self.solar_sv.get()),
            'height_c': int(self.height_sv.get()),
            'albedo_c': float(self.albedo_sv.get()),
            'steffan_c': (4.903*10**(-9))/24,
            'caloric_capacity_c': float(self.caloric_capacity_sv.get()),
            'soil_depth_c': float(self.soil_depth_sv.get()),
            'psicrometric_c': float(self.psicrometric_sv.get())
        }

        start_date: dict[str, str] = {
            'month': self.start_date_month_sv.get(),
            'day': self.start_date_day_sv.get(),
            'year': self.start_date_year_sv.get()
        }

        end_date: dict[str, str] = {
            'month': self.end_date_month_sv.get(),
            'day': self.end_date_day_sv.get(),
            'year': self.end_date_year_sv.get()
        }

        data = self.spreadsheet_data

        result = run_scenario(start_date, end_date, data, constants)
        if result:
            self.get_data_from_cache()
        else:
            self.open_popup()

    def new_input_row(self, frame: tk.Frame, row: int, variable: str, units: str,
                      text_var: tk.StringVar, callback: Callable[[], Any] | None = None,
                      disabled: bool = False) -> None:
        ''' Returns the handle to data entry that was created for the input row '''
        tk.Label(frame, text=variable, padx=10, pady=10).grid(row=row, column=0)
        if callback:
            entry = tk.Entry(frame, textvariable=text_var, validate="key", validatecommand=callback, width=15)
        else:
            entry = tk.Entry(frame, textvariable=text_var, width=15)
        if disabled:
            entry.configure(state="disabled")
        entry.grid(row=row, column=1, columnspan=1)
        tk.Label(frame, text=units, padx=10, pady=10).grid(row=row, column=2)

    def new_location_input_row(self, frame: tk.Frame, row: int, variable: str,
                               first_sv: StringVar, second_sv: StringVar, third_sv: StringVar, 
                               fourth_sv: StringVar, fifth_sv: StringVar, 
                               callback: Callable[[], Any] | None, first_status: bool, 
                               second_status: bool, third_status: bool, fourth_status: bool, 
                               fifth_status: bool) -> None:
        ''' Returns the handle to 5 data entries that were created for the input row '''
        tk.Label(frame, text=variable, padx=5, pady=10).grid(row=row, column=0)
        if callback:
            entry1 = tk.Entry(frame, textvariable=first_sv, validate="key", validatecommand=callback, width=15)
            entry2 = tk.Entry(frame, textvariable=second_sv, validate="key", validatecommand=callback, width=15)
            entry3 = tk.Entry(frame, textvariable=third_sv, validate="key", validatecommand=callback, width=15)
            entry4 = tk.Entry(frame, textvariable=fourth_sv, validate="key", validatecommand=callback, width=15)
            entry5 = tk.Entry(frame, textvariable=fifth_sv, validate="key", validatecommand=callback, width=15)
        else:
            entry1 = tk.Entry(frame, textvariable=first_sv, width=15)
            entry2 = tk.Entry(frame, textvariable=second_sv, width=15)
            entry3 = tk.Entry(frame, textvariable=third_sv, width=15)
            entry4 = tk.Entry(frame, textvariable=fourth_sv, width=15)
            entry5 = tk.Entry(frame, textvariable=fifth_sv, width=15)
        entry1.grid(row=row, column=1)
        entry2.grid(row=row, column=2)
        entry3.grid(row=row, column=3)
        entry4.grid(row=row, column=4)
        entry5.grid(row=row, column=5)
        if first_status: entry1.configure(state="disabled")
        if second_status: entry2.configure(state="disabled")
        if third_status: entry3.configure(state="disabled")
        if fourth_status: entry4.configure(state="disabled")
        if fifth_status: entry5.configure(state="disabled")

    def raise_result_menu(self) -> None:
        self.main_frame.pack()
        self.input_frame.pack_forget()

    def raise_input_menu(self) -> None:
        self.main_frame.pack_forget()
        self.input_frame.pack()

    def get_test_data(self) -> None:
        ''' Obtains data from file selected by user in the openfiledialog '''
        file = tk.filedialog.askopenfilename(title='Abrir archivo con datos',
            filetypes=[('Excel', '*.xlsx'), ('Excel macros', '*.xlsm'), ('CSV', '*.csv')])
        if not file:
            print('Empty file handle')
            return
        self.spreadsheet_data = load_data(file)

    def check_saved_data(self) -> None:
        print(self.spreadsheet_data.keys())
        for index, item in self.spreadsheet_data.items():
            print(index, item)

    def height_callback(self) -> bool:
        height = self.height_sv.get()
        if height != '' and height.isdigit():
            calculated_value = 101.3*(((293-0.0065*int(height))/293)**5.26)
            self.pressure_sv.set("%.2f" % (calculated_value))
            self.psicrometric_sv.set("%.2f" % (0.665*10**(-3)*calculated_value))
        return True

    def location_lat_callback(self) -> bool:
        lat_degrees = self.lat_degrees_sv.get()
        lat_minutes = self.lat_min_sv.get()
        lat_seconds = self.lat_seconds_sv.get()
        if lat_degrees != '' and lat_degrees.isdigit() and lat_minutes != '' and lat_minutes.isdigit() and lat_seconds != '' and lat_seconds.isdigit():
            decimal_degrees = calculate_decimal_degrees(int(lat_degrees), int(lat_minutes), int(lat_seconds))
            self.lat_decimals_sv.set("%.2f" % (decimal_degrees))
            self.lat_rads_sv.set("%.2f" % (deg_2_rad(decimal_degrees)))
        return True

    def location_long_callback(self) -> bool:
        long_degrees = self.long_degrees_sv.get()
        long_minutes = self.long_min_sv.get()
        long_seconds = self.long_seconds_sv.get()
        if long_degrees != '' and long_degrees.isdigit() and long_minutes != '' and long_minutes.isdigit() and long_seconds != '' and long_seconds.isdigit():
            decimal_degrees = calculate_decimal_degrees(int(long_degrees), int(long_minutes), int(long_seconds))
            self.long_decimals_sv.set("%.2f" % (decimal_degrees))
            self.long_rads_sv.set("%.2f" % (deg_2_rad(decimal_degrees)))
        return True

    def center_long_callback(self) -> bool:
        center_long_decimals: str = self.center_long_decimals_sv.get()
        if center_long_decimals != '' and center_long_decimals.isdigit():
            self.center_long_rads_sv.set("%.2f" % (deg_2_rad(float(center_long_decimals))))
        return True

    def get_data_from_cache(self) -> None:
        cache_path: str | None = get_cache_file_path()
        if not cache_path:
            print('Can\'t reach cache file, it may not exist')
            return
        with open(cache_path, newline='\n', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row_index, row in enumerate(spamreader):
                row_frame = tk.Frame(self.result_frame)
                for col_index in range(len(row)):
                    frm = tk.Frame(self.result_frame,width=960, height=100, bd=2, relief=tk.SUNKEN)
                    tk.Label(frm, text=row[col_index], anchor=tk.NW, bg="white", width=15).grid()
                    self.result_frame.create_window(10+(125*col_index),10+(35*row_index), anchor=tk.NW, window=frm)

    def save_results(self) -> None:
        file = filedialog.asksaveasfilename(title='Seleccionar archivo',
            filetypes=[('CSV', '*.csv')])
        if not file:
            print('Empty file handle')
            return
        save_result_to_system(file)

    def open_popup(self) -> None:
        top = tk.Toplevel(self.TKroot)
        top.geometry("250x150")
        top.title("Error")
        tk.Label(top, text= "No se han seleccionado datos!").place(x=40,y=55)

if __name__ == '__main__':
    app: EvapTk = EvapTk()
    app.run()
