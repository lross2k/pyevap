# Pyevap

GUI application that speeds up the process of calculating evapotranspiration given the constants and geolocation parameters, then just load the environment data and run the calculations.

# Setup

*On Linux distros replace `python` for `python3`*

To get all the needed components run, only requirement is having Python 3 installed

```bash
python make.py setup
```

This should create a virtual environment and install everything in it, unless you use a platform that can't be identified.

# Running

```bash
python make.py modern
```

Will use the modern [customtkinter](https://github.com/TomSchimansky/CustomTkinter) library for GUI rendering.

```bash
python make.py legacy
```

Will use the tradition [tkinter](https://github.com/TomSchimansky/CustomTkinter) interface.

# Builing

***Currently only building for Windows platform***

```bash
python make.py build
```

This will build a single `.exe` file for the app.

```bash
python make.py build folder
```

This will build an `.exe` file alongside a folder with all the required includes.

# Developing

## Code quality

This repository uses typing annotations that can be verified via linting with mypy

```bash
python make.py lint
```
