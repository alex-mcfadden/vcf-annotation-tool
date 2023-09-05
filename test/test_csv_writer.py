import os
from io import StringIO
from unittest.mock import patch

import pytest

from csv_writer import write_csv


class TestCsvWriter:
    @pytest.fixture(autouse=True)
    def input_dicts(self):
        return [
            {"chromosome": "1", "position": 1000},
            {"chromosome": "2", "position": 2000},
        ]

    @pytest.fixture(autouse=True)
    def fieldnames(self):
        return ["chromosome", "position"]

    @pytest.fixture(autouse=True)
    def filename(self):
        return "test.csv"

    @pytest.fixture(autouse=True)
    def expected_output(self):
        return "chromosome,position\n1,1000\n2,2000\n"

    def test_write_csv_stdout(self, input_dicts, fieldnames, expected_output):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            write_csv(input_dicts, fieldnames)
            assert mock_stdout.getvalue() == expected_output

    def test_write_csv_file(self, input_dicts, fieldnames, filename, expected_output):
        write_csv(input_dicts, fieldnames, filename=filename)
        with open(filename, "r") as f:
            assert f.read() == expected_output
        os.remove(filename)
