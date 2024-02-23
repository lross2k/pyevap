import os

def main() -> None:
    os.system('./bin/mypy --ignore-missing-imports --strict main.py')

if __name__ == "__main__":
    main()
