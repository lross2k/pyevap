import customtkinter
import openpyxl

# class  

class Evap:

    def __init__(self):
        # Setting the custom theme for the app
        customtkinter.set_default_color_theme('evap.json')

        # Appearance
        customtkinter.set_appearance_mode('system') # 'system' doesn't work on Linux yet, however it works on my GNOME 40

        # Scaling
        # customtkinter.deactivate_automatic_dpi_awareness()
        # customtkinter.set_widget_scaling(float_value)  # widget dimensions and text size
        # customtkinter.set_window_scaling(float_value)  # window geometry dimensions

        self.input_frame = None
        self.main_frame = None
        self.TKroot = customtkinter.CTk()
        self.TKroot.geometry("800x600")
        self.TKroot.title('PyEvap')
        self.gen_input_frame()
        self.gen_main_frame()
        self.main_frame.pack()
        self.spreadsheet_data = {}

    def run(self):
        self.raise_main_menu()
        self.TKroot.mainloop()

    def gen_input_frame(self):
        # Input frame basis
        self.input_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(self.input_frame, text='Input Page').grid(row=0, column=0, columnspan=2)
        customtkinter.CTkButton(self.input_frame, text='Back to Main Page', command=self.raise_main_menu).grid(row=1, column=0, columnspan=2)

        # Values that must be entered by the user
        customtkinter.CTkLabel(self.input_frame, text='Input Page').grid(row=2, column=0, columnspan=2)
        left_localization_data = customtkinter.CTkFrame(self.input_frame, width=500)
        self.new_input_row(left_localization_data, 1, 'Altura', 'msnm')
        self.new_input_row(left_localization_data, 2, 'Albedo', '-')
        self.new_input_row(left_localization_data, 3, 'Constante Solar', 'MJ/m^2 min')
        self.new_input_row(left_localization_data, 4, 'Altura de medición', 'm')
        left_localization_data.grid(row=3, column=0)

        right_localization_data = customtkinter.CTkFrame(self.input_frame)
        self.new_input_row(right_localization_data, 1, 'Altura', 'msnm')
        self.new_input_row(right_localization_data, 2, 'Albedo', '-')
        self.new_input_row(right_localization_data, 3, 'Constante Solar', 'MJ/m^2 min')
        right_localization_data.grid(row=3, column=1)

        # Values defined from other values
        customtkinter.CTkLabel(self.input_frame, text='Valores calculados').grid(row=4, column=0, columnspan=2)

        left_calculated_data = customtkinter.CTkFrame(self.input_frame)
        self.new_input_row(left_calculated_data, 1, 'Presión Atmosférica', 'kPa')
        left_calculated_data.grid(row=5, column=0)

        right_calculated_data = customtkinter.CTkFrame(self.input_frame)
        self.new_input_row(right_calculated_data, 2, 'Constante psicrométrica (ϒ)', 'kPa /°C')
        right_calculated_data.grid(row=5, column=1)

        # Values related to location
        customtkinter.CTkLabel(self.input_frame, text='Ubicación').grid(row=6, column=0, columnspan=2)
        location_data = customtkinter.CTkScrollableFrame(self.input_frame, width=700, height=150, orientation='horizontal')

        customtkinter.CTkLabel(location_data, text='Dirección',         padx=10, pady=10).grid(row=0, column=1)
        customtkinter.CTkLabel(location_data, text='Grados',            padx=10, pady=10).grid(row=0, column=2)
        customtkinter.CTkLabel(location_data, text='Minutos',           padx=10, pady=10).grid(row=0, column=3)
        customtkinter.CTkLabel(location_data, text='Grados decimales',  padx=10, pady=10).grid(row=0, column=4)
        customtkinter.CTkLabel(location_data, text='Radianes',          padx=10, pady=10).grid(row=0, column=5)

        self.new_location_input_row(location_data, 1, 'Latitud (φ)')
        self.new_location_input_row(location_data, 2, 'Longitud (Lm)')
        self.new_location_input_row(location_data, 3, 'Longitud centro (Lz)')

        location_data.grid(row=7, column=0, columnspan=2)

    def gen_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(self.main_frame, text='Main Page').grid(row=0, column=0)
        customtkinter.CTkButton(self.main_frame, text='Go to Input Frame', command=self.raise_input).grid(row=1, column=0)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        customtkinter.CTkButton(self.main_frame, text='Ttes', command=self.check_saved_data).grid(row=2, column=0, columnspan=2)
        customtkinter.CTkButton(self.main_frame, text='Load data', command=self.get_test_data).grid(row=3, column=0, columnspan=2)

    def new_input_row(self, frame, row, variable, units):
        customtkinter.CTkLabel(frame, text=variable, padx=10, pady=10).grid(row=row, column=0)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=1, columnspan=2)
        customtkinter.CTkLabel(frame, text=units, padx=10, pady=10).grid(row=row, column=3)
    
    def new_location_input_row(self, frame, row, variable):
        customtkinter.CTkLabel(frame, text=variable, padx=5, pady=10).grid(row=row, column=0)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=1)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=2)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=3)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=4)
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=5)

    def raise_main_menu(self):
        self.input_frame.pack_forget()
        self.main_frame.pack()

    def raise_input(self):
        self.main_frame.pack_forget()
        self.input_frame.pack()

    def get_test_data(self):
        ''' Obtains data from file selected by user in the openfiledialog '''
        file = customtkinter.filedialog.askopenfilename(title='Abrir archivo con datos', 
            filetypes=[('Excel', '*.xlsx'), ('Excel macros', '*.xlsm'), ('CSV', '*.csv')])
        if not file:
            print('Empty file handle')
            return
        wb = openpyxl.load_workbook(file)
        ws = wb.active if 'Datos' not in wb.get_sheet_names() else wb.get_sheet_by_name('Datos')
        self.spreadsheet_data = {}
        for col in ws['A1:G1'][0]:
            self.spreadsheet_data[col.value] = []
        for col in ws.rows:
            for index in range(len(self.spreadsheet_data.keys())):
                self.spreadsheet_data[list(self.spreadsheet_data.keys())[index]].append(col[index].value)

    def check_saved_data(self):
        print(self.spreadsheet_data.keys())
        for index, item in self.spreadsheet_data.items():
            print(index, item)
