import customtkinter
from customtkinter import StringVar
import openpyxl
from calculations import run_scenario, deg_2_rad
from evapotranspiration import load_data, SoilData, calculate_decimal_degrees
from typing import Callable, Any

class Evap:

    def __init__(self) -> None:
        # Setting the custom theme for the app
        customtkinter.set_default_color_theme('evap.json')

        # Appearance
        customtkinter.set_appearance_mode('system') # 'system' doesn't work on Linux yet, however it
        # works on my GNOME 40, and my KDE Plasma

        # Scaling
        # customtkinter.deactivate_automatic_dpi_awareness()
        # customtkinter.set_widget_scaling(float_value)  # widget dimensions and text size
        # customtkinter.set_window_scaling(float_value)  # window geometry dimensions

        self.TKroot = customtkinter.CTk()
        self.TKroot.geometry("800x600")
        self.TKroot.title('PyEvap')

        self.height_sv: StringVar           = StringVar(value=2129)
        self.albedo_sv: StringVar           = StringVar(value=0.23)
        self.solar_sv: StringVar            = StringVar(value=0.082)
        self.meassure_height_sv: StringVar  = StringVar(value=6.5)
        self.pressure_sv: StringVar         = StringVar(value=78.4)
        self.psicrometric_sv: StringVar     = StringVar(value=0.05)
        self.soil_depth_sv: StringVar       = StringVar(value=0.1)
        self.caloric_capacity_sv: StringVar = StringVar(value=2.1)
        self.highest_point_sv: StringVar    = StringVar(value=12)
        self.lat_degrees_sv: StringVar      = StringVar(value=9)
        self.lat_min_sv: StringVar          = StringVar(value=55)
        self.lat_seconds_sv: StringVar      = StringVar(value=26)
        self.lat_decimals_sv: StringVar     = StringVar(value=calculate_decimal_degrees(int(self.lat_degrees_sv.get()), int(self.lat_min_sv.get()), int(self.lat_seconds_sv.get())))
        self.lat_rads_sv: StringVar         = StringVar(value=deg_2_rad(float(self.lat_decimals_sv.get())))
        self.long_degrees_sv: StringVar     = StringVar(value=83)
        self.long_min_sv: StringVar         = StringVar(value=53)
        self.long_seconds_sv: StringVar     = StringVar(value=48)
        self.long_decimals_sv: StringVar    = StringVar(value=calculate_decimal_degrees(int(self.long_degrees_sv.get()), int(self.long_min_sv.get()), int(self.long_seconds_sv.get())))
        self.long_rads_sv: StringVar        = StringVar(value=deg_2_rad(float(self.long_decimals_sv.get())))

        self.input_frame = self.gen_input_frame()
        self.main_frame = self.gen_main_frame()
        self.main_frame.pack()
        self.spreadsheet_data: SoilData = {'date': [], 'H': [], 'TA': [], 'HR': [], 'VV': [], 'RS': [], 'PR': []}

    def run(self) -> None:
        self.raise_main_menu()
        self.TKroot.mainloop()

    def gen_input_frame(self) -> customtkinter.CTkFrame:
        # Input frame basis
        input_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(input_frame, text='Input Page').grid(row=0, column=0, columnspan=2)
        customtkinter.CTkButton(input_frame, text='Back to Main Page', command=self.raise_main_menu).grid(row=1, column=0, columnspan=2)

        # Values that must be entered by the user
        customtkinter.CTkLabel(input_frame, text='Input Page').grid(row=2, column=0, columnspan=2)
        left_localization_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(left_localization_data, 1, 'Altura', 'msnm', self.height_sv, callback=self.height_callback)
        self.new_input_row(left_localization_data, 2, 'Albedo', '-', self.albedo_sv)
        self.new_input_row(left_localization_data, 3, 'Constante Solar', 'MJ/m^2 min', self.solar_sv)
        self.new_input_row(left_localization_data, 4, 'Altura de medición', 'm', self.meassure_height_sv)
        left_localization_data.grid(row=3, column=0)

        right_localization_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(right_localization_data, 1, 't=punto máximo', '-', self.highest_point_sv)
        self.new_input_row(right_localization_data, 2, 'Capacidad calorífica', 'MJ m-3 °C-1', self.caloric_capacity_sv)
        self.new_input_row(right_localization_data, 3, 'Δz=profundida del suelo', 'm', self.soil_depth_sv)

        right_localization_data.grid(row=3, column=1)

        # Values defined from other values
        customtkinter.CTkLabel(input_frame, text='Valores calculados').grid(row=4, column=0, columnspan=2)

        left_calculated_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(left_calculated_data, 1, 'Presión Atmosférica', 'kPa', self.pressure_sv, disabled=True)
        left_calculated_data.grid(row=5, column=0)

        right_calculated_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(right_calculated_data, 2, 'Constante psicrométrica (ϒ)', 'kPa /°C', self.psicrometric_sv, disabled=True)
        right_calculated_data.grid(row=5, column=1)

        # Values related to location
        customtkinter.CTkLabel(input_frame, text='Ubicación').grid(row=6, column=0, columnspan=2)
        location_data = customtkinter.CTkScrollableFrame(input_frame, width=800, height=150, orientation='horizontal')

        customtkinter.CTkLabel(location_data, text='Dirección',         padx=10, pady=10).grid(row=0, column=1)
        customtkinter.CTkLabel(location_data, text='Grados',            padx=10, pady=10).grid(row=0, column=2)
        customtkinter.CTkLabel(location_data, text='Minutos',           padx=10, pady=10).grid(row=0, column=3)
        customtkinter.CTkLabel(location_data, text='Grados decimales',  padx=10, pady=10).grid(row=0, column=4)
        customtkinter.CTkLabel(location_data, text='Radianes',          padx=10, pady=10).grid(row=0, column=5)

        self.new_location_input_row(location_data, 1, 'Latitud (φ)', self.lat_degrees_sv, self.lat_min_sv, self.lat_seconds_sv,
                                    self.lat_decimals_sv, self.lat_rads_sv, self.location_lat_callback, False, False, False,
                                    True, True)
        self.new_location_input_row(location_data, 2, 'Longitud (Lm)', self.long_degrees_sv, self.long_min_sv, self.long_seconds_sv,
                                    self.long_decimals_sv, self.long_rads_sv, self.location_long_callback, False, False, False,
                                    True, True)
        self.new_location_input_row(location_data, 3, 'Longitud centro (Lz)', None, None, None,
                                    None, None, None, True, True, True,
                                    False, False)

        location_data.grid(row=7, column=0, columnspan=2)
        return input_frame

    def gen_main_frame(self) -> customtkinter.CTkFrame:
        main_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(main_frame, text='Main Page').grid(row=0, column=0)
        customtkinter.CTkButton(main_frame, text='Go to Input Frame', command=self.raise_input).grid(row=1, column=0)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        customtkinter.CTkButton(main_frame, text='Ttes', command=self.check_saved_data).grid(row=2, column=0, columnspan=2)
        customtkinter.CTkButton(main_frame, text='Calculate', command=self.run_scenario_example).grid(row=4, column=1, columnspan=2)
        customtkinter.CTkButton(main_frame, text='Load data', command=self.get_test_data).grid(row=3, column=0, columnspan=2)
        return main_frame

    def run_scenario_example(self) -> None:
        constants = {
            'measure_height_c': float(self.meassure_height_sv.get()),
            'latitude_rad_c': float(self.lat_rads_sv.get()),
            'max_point_c': int(self.highest_point_sv.get()),
            'centre_logitude_deg_c': 90,
            'longitude_deg_c': float(self.long_decimals_sv.get()),
            'solar_c': float(self.solar_sv.get()),
            'height_c': int(self.height_sv.get()),
            'albedo_c': float(self.albedo_sv.get()),
            'steffan_c': (4.903*10**(-9))/24,
            'caloric_capacity_c': float(self.caloric_capacity_sv.get()),
            'soil_depth_c': float(self.soil_depth_sv.get()),
            'psicrometric_c': float(self.psicrometric_sv.get())
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

        data = self.spreadsheet_data

        run_scenario(start_date, end_date, data, constants)

    def new_input_row(self, frame: customtkinter.CTkFrame, row: int, variable: str, units: str,
                      text_var: customtkinter.StringVar, callback: Callable[[], Any] | None = None,
                      disabled: bool = False) -> None:
        ''' Returns the handle to data entry that was created for the input row '''
        customtkinter.CTkLabel(frame, text=variable, padx=10, pady=10).grid(row=row, column=0)
        if callback:
            entry = customtkinter.CTkEntry(frame, textvariable=text_var, validate="key", validatecommand=callback)
        else:
            entry = customtkinter.CTkEntry(frame, textvariable=text_var)
        if disabled:
            entry.configure(state="disabled")
        entry.grid(row=row, column=1, columnspan=1)
        customtkinter.CTkLabel(frame, text=units, padx=10, pady=10).grid(row=row, column=2)

    def new_location_input_row(self, frame: customtkinter.CTkFrame, row: int, variable: str,
                               first_sv: StringVar | None, second_sv: StringVar | None,
                               third_sv: StringVar | None, fourth_sv: StringVar | None,
                               fifth_sv: StringVar | None, callback: Callable[[], Any] | None,
                               first_status: bool, second_status: bool, third_status: bool,
                               fourth_status: bool, fifth_status: bool) -> list[customtkinter.CTkEntry]:
        ''' Returns the handle to 5 data entries that were created for the input row '''
        customtkinter.CTkLabel(frame, text=variable, padx=5, pady=10).grid(row=row, column=0)
        # TODO
        entry1 = customtkinter.CTkEntry(frame, placeholder_text="valor")
        entry2 = customtkinter.CTkEntry(frame, placeholder_text="valor")
        entry3 = customtkinter.CTkEntry(frame, placeholder_text="valor")
        entry4 = customtkinter.CTkEntry(frame, placeholder_text="valor")
        entry5 = customtkinter.CTkEntry(frame, placeholder_text="valor")
        entry1.grid(row=row, column=1)
        entry2.grid(row=row, column=2)
        entry3.grid(row=row, column=3)
        entry4.grid(row=row, column=4)
        entry5.grid(row=row, column=5)
        return [entry1, entry2, entry3, entry4, entry5]

    def raise_main_menu(self) -> None:
        self.input_frame.pack_forget()
        self.main_frame.pack()

    def raise_input(self) -> None:
        self.main_frame.pack_forget()
        self.input_frame.pack()

    def get_test_data(self) -> None:
        ''' Obtains data from file selected by user in the openfiledialog '''
        file = customtkinter.filedialog.askopenfilename(title='Abrir archivo con datos', 
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
            self.lat_decimals_sv.set(decimal_degrees)
            self.lat_rads_sv.set(deg_2_rad(decimal_degrees))
        return True

    def location_long_callback(self) -> bool:
        long_degrees = self.long_degrees_sv.get()
        long_minutes = self.long_min_sv.get()
        long_seconds = self.long_seconds_sv.get()
        if long_degrees != '' and long_degrees.isdigit() and long_minutes != '' and long_minutes.isdigit() and long_seconds != '' and long_seconds.isdigit():
            decimal_degrees = calculate_decimal_degrees(int(long_degrees), int(long_minutes), int(long_seconds))
            self.long_decimals_sv.set(decimal_degrees)
            self.long_rads_sv.set(deg_2_rad(decimal_degrees))
        return True
