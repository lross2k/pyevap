from setup import setup
from sys import argv
import os

def platform_path(original_path: str, os_name: str) -> str:
    final_path: str = original_path
    if os_name == 'nt':
        final_path = final_path.replace('/bin/', '\\Scripts\\')
        final_path = final_path.replace('/', '\\')
    return final_path

def main() -> None:
    os_name: str = os.name

    if len(argv) == 1:
        os.system(platform_path('./bin/python operations.py legacy', os_name))
        return

    args = argv[1:]

    match(args[0]):
        case 'setup':
            setup(os_name)
        case 'lint':
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict operations.py', os_name))
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict make.py', os_name))
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict evapguitk.py', os_name))
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict evapgui.py', os_name))
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict common.py', os_name))
            os.system(platform_path('./bin/mypy --ignore-missing-imports --strict evapotranspiration.py', os_name))
        case 'legacy':
            os.system(platform_path('./bin/python operations.py legacy', os_name))
        case 'modern':                                               
            os.system(platform_path('./bin/python operations.py modern', os_name))

if __name__ == '__main__':
    main()
