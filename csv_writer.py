import csv
import sys


def write_csv(input_dicts, fieldnames, filename=None):
    if not filename:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in input_dicts:
            writer.writerow(row)
    else:
        with open(filename, mode="w", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in input_dicts:
                writer.writerow(row)
