from evapgui import Evap
from evapguitk import EvapTk
import sys

def main() -> None:
    if sys.argv[1] == 'modern':
        app = Evap()
    elif sys.argv[1] == 'legacy':
        app = EvapTk()
    app.run()

if __name__ == '__main__':
    main()
