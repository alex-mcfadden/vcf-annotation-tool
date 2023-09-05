import os
from vcf_parser import parser

import pytest


class TestParser:
    @pytest.fixture(autouse=True)
    def filename(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures/test_vcf_data.txt"
        )

    @pytest.fixture(autouse=True)
    def expected_output(self):
        return [
            {
                "CHROM": "1",
                "POS": 6219287,
                "ID": None,
                "REF": "TCACACA",
                "ALT": "TCACA",
                "QUAL": 2997,
                "FILTER": [],
                "BRF": 0.35,
                "HP": 1,
                "HapScore": [1],
                "MGOF": [6],
                "MMLQ": 23.0,
                "MQ": [51.91],
                "QD": 20.0,
                "SC": "TGAGACTCCATCACACACACA",
                "SbPval": [1.0],
                "Source": ["Platypus"],
                "TC": 172,
                "TCF": 170,
                "TCR": 2,
                "WE": 6219302,
                "WS": 6219277,
                "start": 6219286,
                "end": 6219293,
                "FR": 0.5,
                "TR": 108,
                "NF": 108,
                "NR": 0,
                "PP": 2997.0,
                "variant_frequency": 0.627906976744186,
                "hgvs_notation": "1:g.6219287TCACACA>TCACA",
            },
            {
                "CHROM": "1",
                "POS": 6219287,
                "ID": None,
                "REF": "TCACACA",
                "ALT": "T",
                "QUAL": 2997,
                "FILTER": [],
                "BRF": 0.35,
                "HP": 1,
                "HapScore": [1],
                "MGOF": [6],
                "MMLQ": 23.0,
                "MQ": [51.91],
                "QD": 20.0,
                "SC": "TGAGACTCCATCACACACACA",
                "SbPval": [1.0],
                "Source": ["Platypus"],
                "TC": 172,
                "TCF": 170,
                "TCR": 2,
                "WE": 6219302,
                "WS": 6219277,
                "start": 6219286,
                "end": 6219293,
                "FR": 0.5,
                "TR": 108,
                "NF": 108,
                "NR": 0,
                "PP": 2652.0,
                "variant_frequency": 0.627906976744186,
                "hgvs_notation": "1:g.6219287TCACACA>T",
            },
            {
                "CHROM": "1",
                "POS": 1246004,
                "ID": None,
                "REF": "A",
                "ALT": "G",
                "QUAL": 2965,
                "FILTER": [],
                "BRF": 0.09,
                "HP": 6,
                "HapScore": [1],
                "MGOF": [5],
                "MMLQ": 32.0,
                "MQ": [59.5],
                "QD": 20.0,
                "SC": "ACAGGTACGTATTTTTCCAGG",
                "SbPval": [0.62],
                "Source": ["Platypus"],
                "TC": 152,
                "TCF": 101,
                "TCR": 51,
                "WE": 1246012,
                "WS": 1245994,
                "start": 1246003,
                "end": 1246004,
                "FR": 1.0,
                "TR": 148,
                "NF": 101,
                "NR": 47,
                "PP": 2965.0,
                "variant_frequency": 0.9736842105263158,
                "hgvs_notation": "1:g.1246004A>G",
            },
        ]

    def test_parser(self, filename, expected_output):
        output_data = parser(filename)
        assert output_data == expected_output
