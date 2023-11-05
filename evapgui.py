import customtkinter

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
        self.gen_input_frame()
        self.gen_main_frame()
        self.main_frame.pack()

    def run(self):
        self.raise_main_menu()
        self.TKroot.mainloop()

    def gen_input_frame(self):
        self.input_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(self.input_frame, text='Input Page').grid(row=0, column=0)
        customtkinter.CTkButton(self.input_frame, text='Go to Main Page', command=self.raise_main_menu).grid(row=0, column=1)

        self.new_input_row(self.input_frame, 1, 'Altura', 'msnm')
        self.new_input_row(self.input_frame, 2, 'Albedo', '-')
        self.new_input_row(self.input_frame, 3, 'Constante Solar', 'MJ/m^2 min')

    def gen_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self.TKroot)
        customtkinter.CTkLabel(self.main_frame, text='Main Page').grid(row=0, column=0)
        customtkinter.CTkButton(self.main_frame, text='Go to Input Frame', command=self.raise_input).grid(row=1, column=0)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

    def new_input_row(self, frame, row, variable, units):
        customtkinter.CTkLabel(frame, text=variable, padx=20, pady=20).grid(row=row, column=0, sticky='w')
        customtkinter.CTkEntry(frame, placeholder_text="valor").grid(row=row, column=1, columnspan=2)
        customtkinter.CTkLabel(frame, text=units, padx=20, pady=20).grid(row=row, column=3, sticky='e')

    def raise_main_menu(self):
        self.input_frame.pack_forget()
        self.main_frame.pack()

    def raise_input(self):
        self.main_frame.pack_forget()
        self.input_frame.pack()

def open_file():
    customtkinter.filedialog.askopenfilename()
