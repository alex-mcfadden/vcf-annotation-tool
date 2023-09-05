"""
Utilities for parsing Ensembl variant responses, and creating request bodies for Ensemble API calls.
"""
from constants import *


def create_hgvs_notation(chrom, pos, ref, alt, prefix="g"):
    # Puts together HGVS notation from the variant data, i.e.
    # 1:g.123456A>T for a variant on chromosome 1 at position 123456 with ref A and alt T.
    return f"{chrom}:{prefix}.{pos}{ref}>{alt}"


def get_maf(variant):
    # search the colocated_variants for the one with the MAF present.
    # If none are present, return "Not Found"
    colocated_variants = variant.get(COLOCATED_VARIANTS, [])
    for cv in colocated_variants:
        if MINOR_ALLELE_FREQ in cv.keys():
            return cv[MINOR_ALLELE_FREQ]
    return NOT_FOUND


def chunks(lst, n):
    # Yield successive n-sized chunks from lst.
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
