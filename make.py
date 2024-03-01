from sys import argv
from operations import setup, lint, run

def main():
    if len(argv) == 1:
        run(legacy=True)
        return

    args = argv[1:]

    match(args[0]):
        case 'setup':
            setup()
        case 'lint':
            lint()
        case 'legacy':
            run(legacy=True)
        case 'modern':
            run(legacy=False)

if __name__ == '__main__':
    main()
