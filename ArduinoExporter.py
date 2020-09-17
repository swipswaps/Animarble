'''
This program converts a .msync file into a corresponding Arduino .h file
'''

import csv
import os
import argparse

from utils import create_unique_filename

''' Constants '''
MOVEMENT_FUNCTION = 'marbleSynchronizer.moveMarbles'

ap = argparse.ArgumentParser(
    description="Convert a .msync file to an Arduino .h file")
ap.add_argument('input', help="The input .msync file to process")
ap.add_argument('-o', '--output', help="The output .h file to write to")
ap.add_argument('-f', '--function',
                help='The function name to contain the Arduino code in')

args = ap.parse_args()

msync_file = args.input

output_filename = None
if args.output is None:
    output_filename = create_unique_filename(
        f"outputs/ArduinoExporter/{os.path.splitext(os.path.basename(msync_file))[0]}.h")
else:
    output_filename = args.output

function_name = None
if args.function is None:
    function_name = "GeneratedRoutine"
else:
    function_name = args.function


def main():
    with open(output_filename, "w+") as output_file:
        print("// File auto-generated by ArduinoExporter.py", file=output_file)
        print(f"void {function_name}() {{", file=output_file)

        with open(msync_file) as input_file:
            msync_reader = csv.DictReader(input_file)
            for i, row in enumerate(msync_reader):
                if (i % 2 == 1):
                    continue

                # Include comment indicating which row the command was generated from
                print(f"\t// Row {i}", file=output_file)

                # Write command, taking care to treat timestamp as a Long
                print(
                    (
                        f"\t{MOVEMENT_FUNCTION}("
                        f"{round(int(row['timestamp']))}L,"
                        f" {round(int(row['left_pan']))},"
                        f" {round(int(row['left_tilt']))},"
                        f" {round(int(row['right_pan']))},"
                        f" {round(int(row['right_tilt']))}"
                        f");"
                    ),
                    file=output_file)
                print(file=output_file)

        print('}', file=output_file)

    print(f"Arduino code exported to: {output_filename}")


if __name__ == '__main__':
    main()
