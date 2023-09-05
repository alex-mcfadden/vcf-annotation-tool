import os
from io import StringIO
from unittest.mock import patch

import pytest

from vcf_annotation import annotate


class TestAnnotate:
    @pytest.fixture(autouse=True)
    def filename(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures/test_vcf_data.txt"
        )

    @pytest.fixture(autouse=True)
    def output_filename(self):
        return "test.csv"

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
    def output_file_data(self):
        return "most_severe_consequence,minor_allele_freq\nmissense_variant,0.01\nsynonymous_variant,0.05\n"

    def test_annotate_stdout(self, filename, mock_annotations, output_file_data):
        with patch("vcf_annotation.fetch_annotations", return_value=mock_annotations):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                data = annotate(filename)
                assert len(data) == 2
                assert mock_stdout.getvalue() == output_file_data

    def test_annotate_to_file(
        self, filename, output_filename, mock_annotations, output_file_data
    ):
        with patch("vcf_annotation.fetch_annotations", return_value=mock_annotations):
            data = annotate(filename, output=output_filename)
            assert len(data) == 2
            with open(output_filename, "r") as f:
                assert f.read() == output_file_data

            os.remove(output_filename)

    def test_annotate_no_write(self, filename, output_filename, mock_annotations):
        with patch("vcf_annotation.fetch_annotations", return_value=mock_annotations):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                data = annotate(filename, write_to_csv=False)
                assert len(data) == 2
                assert not os.path.exists(output_filename)
                assert not mock_stdout.getvalue()
