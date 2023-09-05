import json
import sys

import requests

from constants import *
from util import chunks, get_maf


def fetch_annotations(vcf_data: list[dict], excluded: list[str] = None) -> list[dict]:
    """
    Chunks input VCF data into requests of size MAX_REQUEST_SIZE,
    creates HGVS notations, and fetches annotations from Ensembl
    via the notations, adding them to the original dict.
    Returns a list of dicts with the annotations added.

    Args:
        vcf_data: a list of dicts with VCF data
        excluded: a list of fields to exclude from the return data
    Returns:
        out_data: a list of dicts with Ensembl variant annotations added
    """
    if excluded is None:
        excluded = DEFAULT_EXCLUDED_FIELDS
    data_chunks = chunks(vcf_data, MAX_REQUEST_SIZE)
    out_data = []
    for chunk in data_chunks:
        response = fetch_response(chunk)
        for i, variant in enumerate(response):
            if variant.get(TRANSCRIPT_CONSEQUENCES):  # there are genes affected
                for tc in variant[TRANSCRIPT_CONSEQUENCES]:
                    data = chunk[i].copy()
                    data[GENE_SYMBOL] = tc[GENE_SYMBOL]
                    data[CONSEQUENCE_TERMS] = tc[CONSEQUENCE_TERMS]
                    data[MOST_SEVERE_CONSEQUENCE] = variant[MOST_SEVERE_CONSEQUENCE]
                    data[MINOR_ALLELE_FREQ] = get_maf(variant)
                    data[BIOTYPE] = tc[BIOTYPE]
                    data[TRANSCRIPT_ID] = tc[TRANSCRIPT_ID]
                    data[GENE_ID] = tc[GENE_ID]
                    out_data.append(data)
            else:  # only intergenic, no genes affected
                data = chunk[i].copy()
                data[GENE_SYMBOL] = INTERGENIC_MESSAGE
                data[MOST_SEVERE_CONSEQUENCE] = variant[MOST_SEVERE_CONSEQUENCE]
                data[MINOR_ALLELE_FREQ] = get_maf(variant)
                out_data.append(chunk[i])

    for data in out_data: # remove user-specified fields from output
        for field in excluded:
            if field in data.keys():
                del data[field]
    return out_data


def fetch_response(chunk: list[dict]) -> list[dict]:
    data_dict = {HGVS_NOTATIONS: [v[HGVS_NOTATION] for v in chunk]}
    r = requests.post(ENSEMBL_REST_SERVER, headers=HEADERS, data=json.dumps(data_dict))
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    return r.json()
