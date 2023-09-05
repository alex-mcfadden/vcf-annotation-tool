import os
from io import StringIO
from unittest.mock import patch

import pytest

from cli import create_args, main


class TestCLI:
    @pytest.fixture(autouse=True)
    def filename(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures/test_vcf_data.txt"
        )

    @pytest.fixture(autouse=True)
    def mock_annotations(self):
        return [
            {"most_severe_consequence": "missense_variant", "minor_allele_freq": 0.01},
            {
                "most_severe_consequence": "synonymous_variant",
                "minor_allele_freq": 0.05,
            },
        ]

    @pytest.fixture(autouse=True)
    def mock_parser_return(self):
        return [
            {"chromosome": "1", "position": 1000},
            {"chromosome": "2", "position": 2000},
        ]

    @pytest.fixture(autouse=True)
    def expected_output(self):
        return "most_severe_consequence,minor_allele_freq\nmissense_variant,0.01\nsynonymous_variant,0.05\n"

    def test_main_stdout(
        self, filename, mock_annotations, expected_output, mock_parser_return
    ):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with patch("cli.fetch_annotations", return_value=mock_annotations):
                with patch("vcf_parser.parser", return_value=mock_parser_return):
                    main(filename)
                    assert mock_stdout.getvalue() == expected_output

    def test_main_file(
        self, filename, mock_annotations, mock_parser_return, expected_output
    ):
        with patch("cli.fetch_annotations", return_value=mock_annotations):
            with patch("vcf_parser.parser", return_value=mock_parser_return):
                main(filename, output="test.csv")
                with open("test.csv", "r") as f:
                    assert f.read() == expected_output
                os.remove("test.csv")

    def test_main_no_args(self):
        with pytest.raises(TypeError):
            main()

    def test_create_args(self):
        with patch("sys.argv", ["cli.py", "test.txt", "--output", "test.csv"]):
            args = create_args()
            assert args.filename == "test.txt"
            assert args.output == "test.csv"

    def test_create_args_stdout(self):
        with patch("sys.argv", ["cli.py", "test.txt"]):
            args = create_args()
            assert args.filename == "test.txt"
            assert args.output == None

    def test_create_args_with_excluded_fields(self):
        with patch(
            "sys.argv",
            ["cli.py", "test.txt", "--excluded_fields", "CHROM", "POS", "ID"],
        ):
            args = create_args()
            assert args.filename == "test.txt"
            assert args.output == None
            assert args.excluded_fields == ["CHROM", "POS", "ID"]
