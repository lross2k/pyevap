from evapgui import Evap
from evapguitk import EvapTk
import os, sys

def run(legacy: bool=True) -> None:
    app: EvapTk | Evap = EvapTk() if legacy else Evap()
    app.run()

if __name__ == '__main__':
    run(legacy=(sys.argv[1] == "legacy"))
