from setup import setup
from sys import argv
import os

def main():
    if len(argv) == 1:
        os.system('./bin/python operations.py legacy')
        return

    args = argv[1:]

    match(args[0]):
        case 'setup':
            setup()
        case 'lint':
            os.system('./bin/mypy --ignore-missing-imports --strict operations.py')
        case 'legacy':
            os.system('./bin/python operations.py legacy')
        case 'modern':
            os.system('./bin/python operations.py modern')

if __name__ == '__main__':
    main()
