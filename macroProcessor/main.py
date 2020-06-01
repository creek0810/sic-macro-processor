import sys
from macroProcessor import MacroProcessor


if __name__ == "__main__":
    arg = sys.argv
    if len(arg) != 2:
        print("Please enter file path")
    else:
        processor = MacroProcessor(arg[1])
        processor.process()
