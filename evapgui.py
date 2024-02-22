import customtkinter
import openpyxl
from calculations import run_scenario
from evapotranspiration import load_data, SoilData

class Evap:

    def __init__(self) -> None:
        # Setting the custom theme for the app
        customtkinter.set_default_color_theme('evap.json')

        # Appearance
        customtkinter.set_appearance_mode('system') # 'system' doesn't work on Linux yet, however it works on my GNOME 40

        # Scaling
        # customtkinter.deactivate_automatic_dpi_awareness()
        # customtkinter.set_widget_scaling(float_value)  # widget dimensions and text size
        # customtkinter.set_window_scaling(float_value)  # window geometry dimensions

        self.height_value: int           = 2129
        self.albedo_value: float           = 0.23
        self.solar_value: float            = 0.082
        self.meassure_height_value: float  = 6.5

        self.height_entry           = None
        self.albedo_entry           = None
        self.solar_entry            = None
        self.meassure_height_entry  = None

        self.TKroot = customtkinter.CTk()
        self.TKroot.geometry("800x600")
        self.TKroot.title('PyEvap')
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
        left_localization_data = customtkinter.CTkFrame(input_frame, width=500)
        self.height_entry = self.new_input_row(left_localization_data, 1, 'Altura', 'msnm', str(self.height_value))
        self.albedo_entry = self.new_input_row(left_localization_data, 2, 'Albedo', '-', str(self.albedo_value))
        self.solar_entry = self.new_input_row(left_localization_data, 3, 'Constante Solar', 'MJ/m^2 min', str(self.solar_value))
        self.meassure_height_entry = self.new_input_row(left_localization_data, 4, 'Altura de medición', 'm', str(self.meassure_height_value))
        print("just defined", self.meassure_height_entry.get())
        left_localization_data.grid(row=3, column=0)

        right_localization_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(right_localization_data, 1, 'Altura', 'msnm', "TODO")
        self.new_input_row(right_localization_data, 2, 'Albedo', '-', "TODO")
        self.new_input_row(right_localization_data, 3, 'Constante Solar', 'MJ/m^2 min', "TODO")
        right_localization_data.grid(row=3, column=1)

        # Values defined from other values
        customtkinter.CTkLabel(input_frame, text='Valores calculados').grid(row=4, column=0, columnspan=2)

        left_calculated_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(left_calculated_data, 1, 'Presión Atmosférica', 'kPa', "TODO")
        left_calculated_data.grid(row=5, column=0)

        right_calculated_data = customtkinter.CTkFrame(input_frame)
        self.new_input_row(right_calculated_data, 2, 'Constante psicrométrica (ϒ)', 'kPa /°C', "TODO")
        right_calculated_data.grid(row=5, column=1)

        # Values related to location
        customtkinter.CTkLabel(input_frame, text='Ubicación').grid(row=6, column=0, columnspan=2)
        location_data = customtkinter.CTkScrollableFrame(input_frame, width=700, height=150, orientation='horizontal')

        customtkinter.CTkLabel(location_data, text='Dirección',         padx=10, pady=10).grid(row=0, column=1)
        customtkinter.CTkLabel(location_data, text='Grados',            padx=10, pady=10).grid(row=0, column=2)
        customtkinter.CTkLabel(location_data, text='Minutos',           padx=10, pady=10).grid(row=0, column=3)
        customtkinter.CTkLabel(location_data, text='Grados decimales',  padx=10, pady=10).grid(row=0, column=4)
        customtkinter.CTkLabel(location_data, text='Radianes',          padx=10, pady=10).grid(row=0, column=5)

        self.new_location_input_row(location_data, 1, 'Latitud (φ)')
        self.new_location_input_row(location_data, 2, 'Longitud (Lm)')
        self.new_location_input_row(location_data, 3, 'Longitud centro (Lz)')

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
        if self.meassure_height_entry.get():
            self.meassure_height_value = float(self.meassure_height_entry.get())
        if self.height_entry.get():
            self.height_value = int(self.height_entry.get())
        if self.albedo_entry.get():
            self.albedo_value = float(self.albedo_entry.get())
        if self.solar_entry.get():
            self.solar_value = float(self.solar_entry.get())

        constants = {
            'measure_height_c': self.meassure_height_value,
            'latitude_rad_c': 0.173,
            'max_point_c': 12,
            'centre_logitude_deg_c': 90,
            'longitude_deg_c': 83.9,
            'solar_c': self.solar_value,
            'height_c': self.height_value,
            'albedo_c': self.albedo_value,
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

        data = self.spreadsheet_data

        run_scenario(start_date, end_date, data, constants)

    def new_input_row(self, frame: customtkinter.CTkFrame, row: int, variable: str, units: str, placeholder: str) -> customtkinter.CTkEntry:
        ''' Returns the handle to data entry that was created for the input row '''
        customtkinter.CTkLabel(frame, text=variable, padx=10, pady=10).grid(row=row, column=0)
        entry = customtkinter.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=row, column=1, columnspan=2)
        customtkinter.CTkLabel(frame, text=units, padx=10, pady=10).grid(row=row, column=3)
        return entry
    
    def new_location_input_row(self, frame: customtkinter.CTkFrame, row: int, variable: str) -> list[customtkinter.CTkEntry]:
        ''' Returns the handle to 5 data entries that were created for the input row '''
        customtkinter.CTkLabel(frame, text=variable, padx=5, pady=10).grid(row=row, column=0)
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
