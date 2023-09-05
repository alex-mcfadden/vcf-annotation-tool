# a CLI for the parser - takes a required filename arg and options,
# and returns a tab-delimited CSV as stdout

import argparse
from vcf_parser import parser

from api_client import fetch_annotations
from constants import *
from csv_writer import write_csv


def create_args():
    parser = argparse.ArgumentParser(
        description="Parse a VCF file and return a tab-delimited CSV with annotations"
    )
    parser.add_argument(
        "filename", type=str, help="the filename of the VCF file to parse"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="the filename of the CSV file to write to, If not specified, will write to stdout",
    )
    parser.add_argument(
        "--excluded_fields",
        nargs="*",
        type=str,
        help="VCF fields to exclude from the output",
    )
    return parser.parse_args()


def main(filename, output=None, excluded_fields=None):
    if excluded_fields is None:
        excluded_fields = DEFAULT_EXCLUDED_FIELDS
    vcf_data = parser(filename)
    annotations = fetch_annotations(vcf_data, excluded=excluded_fields)
    write_csv(annotations, annotations[0].keys(), filename=output)


if __name__ == "__main__":
    parsed_args = create_args()
    main(parsed_args.filename, parsed_args.output, parsed_args.excluded_fields)
