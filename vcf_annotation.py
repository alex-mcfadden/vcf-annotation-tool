from vcf_parser import parser

from api_client import fetch_annotations
from constants import *
from csv_writer import write_csv


def annotate(
    filename: str,
    output: str = None,
    write_to_csv: bool = True,
    excluded_fields: list = None,
):
    if excluded_fields is None:
        excluded_fields = DEFAULT_EXCLUDED_FIELDS
    # method to parse and annotate VCF inputs and write to a CSV or stdout
    parsed_data = parser(filename)
    annotated_data = fetch_annotations(parsed_data, excluded=excluded_fields)
    if write_to_csv:
        write_csv(annotated_data, annotated_data[0].keys(), filename=output)
    return annotated_data
