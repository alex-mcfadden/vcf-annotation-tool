# API Client constants
ENSEMBL_REST_SERVER = "https://grch37.rest.ensembl.org/vep/human/hgvs"  # use the grch37 server to match the genome version
# other URLs can go here for other genome versions


HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
MAX_REQUEST_SIZE = 300
HGVS_NOTATIONS = "hgvs_notations"
HGVS_NOTATION = "hgvs_notation"

# Response object keys
COLOCATED_VARIANTS = "colocated_variants"
TRANSCRIPT_CONSEQUENCES = "transcript_consequences"
INTERGENIC_CONSEQUENCES = "intergenic_consequences"
MOST_SEVERE_CONSEQUENCE = "most_severe_consequence"
GENE_SYMBOL = "gene_symbol"
CONSEQUENCE_TERMS = "consequence_terms"
MINOR_ALLELE_FREQ = "minor_allele_freq"
INTERGENIC_VARIANT = "intergenic_variant"
BIOTYPE = "biotype"
TRANSCRIPT_ID = "transcript_id"
GENE_ID = "gene_id"

# Error messages
NOT_FOUND = "Not found"
INTERGENIC_MESSAGE = "intergenic - no gene"

# Default excluded fields in output data
DEFAULT_EXCLUDED_FIELDS = [
    "QUAL",
    "FILTER",
    "BRF",
    "HP",
    "HapScore",
    "MGOF",
    "MMLQ",
    "MQ",
    "QD",
    "SC",
    "SbPVal",
    "Source",
]
