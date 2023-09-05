import vcf

from util import create_hgvs_notation


def parser(filename: str):
    """
    Method to parse a VCF file into a list of dictionaries,
    where each dictionary represents a variant in the VCF file. Data on
    quality and other metrics are included in the dictionary. Additionally,
    calculated variant frequency and HGVS notation are included in the dictionary.

    Inputs:

        filename: the filename of the VCF file to parse
        excluded: a list of keys to exclude from the output dictionary, for unwanted data

    Returns:
        vcf_data:
            a list of dictionaries, where each dictionary represents a variant in the VCF file.
    """
    vcf_reader = vcf.Reader(open(filename, "r"))
    vcf_data = []

    for record in vcf_reader:
        for i, alt in enumerate(record.ALT):
            variant_data = {
                "CHROM": record.CHROM,
                "POS": record.POS,
                "ID": record.ID,
                "REF": record.REF,
                "ALT": str(alt),
                "QUAL": record.QUAL,
                "FILTER": record.FILTER,
                "BRF": record.INFO["BRF"],
                "HP": record.INFO["HP"],
                "HapScore": record.INFO["HapScore"],
                "MGOF": record.INFO["MGOF"],
                "MMLQ": record.INFO["MMLQ"],
                "MQ": record.INFO["MQ"],
                "QD": record.INFO["QD"],
                "SC": record.INFO["SC"],
                "SbPval": record.INFO["SbPval"],
                "Source": record.INFO["Source"],
                "TC": record.INFO["TC"],
                "TCF": record.INFO["TCF"],
                "TCR": record.INFO["TCR"],
                "WE": record.INFO["WE"],
                "WS": record.INFO["WS"],
                "start": record.start,
                "end": record.end,
                "FR": record.INFO["FR"][i],  # split lists into each variant's value
                "TR": record.INFO["TR"][i],
                "NF": record.INFO["NF"][i],
                "NR": record.INFO["NR"][i],
                "PP": record.INFO["PP"][i],
                "variant_frequency": record.INFO["TR"][i] / record.INFO["TC"],
                "hgvs_notation": create_hgvs_notation(
                    record.CHROM, record.POS, record.REF, alt
                ),
            }
            vcf_data.append(variant_data)

    return vcf_data
