from evapgui import Evap
from evapguitk import EvapTk
import sys, os, platform

def setup():
    if os.name == 'nt':
        if 'pyveng.cfg' not in os.listdir():
            os.system('python -m venv .')
        else:
            print("Directory already contains a virtual environmet")
        os.system('.\Scripts\pip install customtkinter openpyxl mypy')
    elif os.name == 'posix':
        # when running under Debian 12 I found the need for some extra work
        if 'debian' in os.uname().version.lower():
            os.system('apt-get install python3-venv python3-tk -y')
            os.system('python3 -m venv .')
        elif 'arch' in platform.freedesktop_os_release()['ID']:
            if 'pyvenv.cfg' not in os.listdir():
                os.system('pacman -S tk')
                os.system('python -m venv .')
            else:
                print("Directory already contains a virtual environmet")
        else:
            os.system('pip3 install customtkinter openpyxl')
        os.system('./bin/pip install customtkinter openpyxl mypy')

def lint() -> None:
    os.system('./bin/mypy --ignore-missing-imports --strict main.py')

def run(legacy=True) -> None:
    app = EvapTk() if legacy else Evap()
    app.run()

if __name__ == '__main__':
    print('Havent implemented this yet')
