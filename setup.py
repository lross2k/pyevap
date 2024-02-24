import os, platform

if os.name == 'nt':
    os.system('pip install customtkinter openpyxl')
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

