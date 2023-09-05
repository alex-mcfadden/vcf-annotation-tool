# HGVS Annotation Tool

## Introduction

This tool is designed to annotate human genomic variants from an input VCF file, adding 
additional information and returning a CSV output with the additional annotations for 
each variant and each affected gene. The tool is designed to be run on a local machine, 
and requires a working installation of Python 3.8 or higher. Using a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended. 


## Quick Start


As a script: 

```bash
pip install -r requirements.txt
python3 cli.py path/to/input.vcf > path/to/output.csv
```

Or as a library:

```bash
pip install .
```
    
```python
from vcf_annotation import annotate
annotate('path/to/input.vcf', 'path/to/output.csv)
```
## Installation

This tool can be installed as a package, or run as a Python script.

### Package Installation    

To install the package, clone the repository and run the following command from the
root directory of the repository:

```bash
pip install .
```

This will install the package and all of its dependencies. From here, you can import 
various parts of the script like so:

```python
from vcf_annotation import api_client

api_client.fetch_annotations(...)
```

### Script Installation

To run the script in lieu of package installation, clone the repository and run the following command from the root directory of the repository:

```bash
pip3 install -r requirements.txt
```

## Usage

This tool expects an input VCF file made from the [GrCh37](https://grch37.ensembl.org/index.html) reference genome. The tool will annotate each variant in the VCF file by accessing the [Ensembl REST API](https://grch37.rest.ensembl.org) to retrieve the following information:

- HGVS notation
- Gene Symbol
- Minor Allele Frequency (MAF)


This data is collected and returned as a comma-separated values, either as a CSV file 
or as stdout if no filename is supplied (this allows the user to pipe the output to 
another program).

### Command Line Arguments

The tool can be run from the command line with an input file argument::

```bash
    python3 cli.py "path/to/input.vcf"
```

This will create a CSV string, and the output will be sent to stdout. You can
create a CSV file by piping the output to a file path:

```bash
    python3 cli.py path/to/input.vcf > path/to/output.csv
```

### Python Library

The tool can also be run inside another Python program, by importing and using the `annotate()` function. This function takes the following parameters:

- `input_path`: the path to the input VCF file
- `output_path`: the path to the output CSV file (optional)
- `excluded_fields`: a list of column names to exclude from the output CSV file (optional)
- `write_csv`: a boolean indicating whether to write the CSV file to the output path (optional, default True)

```python
from vcf_annotation import annotate

annotation_data = annotate("path/to/input.vcf", "path/to/output.csv") # to file
annotation_data = annotate("path/to/input.vcf") # to stdout
annotation_data = annotate("path/to/input.vcf", excluded_fields=['ID', 'TR']) # remove ID and TR columns

```

This function will return a list of dictionaries, where each dictionary represents a given variant's predicted effect. The keys of the dictionary are the column names of the output
CSV file, and the values are the annotations for each variant effect. 

This method also writes a CSV file to the specified output path.If no output path is specified, the CSV is passed to stdout. You can disable this output altogether by passing the `write_csv=False` parameter:

```python
from vcf_annotation import annotate

annotation_data = annotate("path/to/input.vcf", excluded_fields=['ID', 'TR'], write_csv=False) 
# just return the data, no output file or stdout
```

## Output format

The output of this tool is CSV data, with one row for every predicted genetic variant effect. If a variant has more than one predicted effect (aka consequence), each effect has its own row. Some variants will have no predicted consequences, and these variants get one row with no data for the consequences and gene symbols. Each row is populated with the following columns:

- the original VCF information (i.e. CHROM, TC, TR, POS, REF, ALT), one column each
- variant_frequency: Variant Frequency (defined as TR for the variant/ TC)
- hgvs_notation: HGVS Notation
- gene_symbol: Gene Symbol for the variant's predicted transcript consequences
- consequence_terms: consequence terms describing the type of change the variant causes
- most_severe_consequence: Most Severe Consequence predicted by Ensembl
- minor_allele_freq: Minor Allele Frequency (MAF) from Ensembl
- biotype: the biotype of the predicted transcript
- transcript_id: Transcript ID (Ensembl ENST format)
- gene_id: Gene ID (Ensembl ENSG format)

You can remove any number of these columns by using the `--excluded_fields` parameter:

```bash
python3 cli.py path/to/input.vcf --excluded_fields ID TR > path/to/output.csv
```

The above example will remove the ID and TR columns from the output CSV file. If this parameter is not specified, a default set of columns will be used (see [constants.py](./constants.py#L29)). To use all available columns:

```bash
python3 cli.py path/to/input.vcf --excluded_fields None > path/to/output.csv
```


## Testing

To run unit tests, make sure to install the dependencies from requirements.txt. Then run the following command from the root directory of the repository:

```bash
pytest test
```

This runs all unit tests in the test/ folder, which includes a small fixture VCF file. Calls to the Ensembl server are mocked here. 