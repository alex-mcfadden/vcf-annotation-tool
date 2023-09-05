from unittest.mock import patch

import pytest

from api_client import fetch_annotations, fetch_response


class TestApiClient:
    @pytest.fixture(autouse=True)
    def test_data(self):
        return [
            {
                "chrom": "1",
                "pos": 100,
                "ref": "A",
                "alt": "T",
                "total_coverage": 100,
                "variant_coverage": 50,
                "variant_frequency": 0.5,
                "hgvs_notation": "NC_000001.11:g.100A>T",
            },
            {
                "chrom": "1",
                "pos": 200,
                "ref": "C",
                "alt": "G",
                "total_coverage": 100,
                "variant_coverage": 50,
                "variant_frequency": 0.5,
                "hgvs_notation": "NC_000001.11:g.200C>G",
            },
        ]

    @pytest.fixture(autouse=True)
    def mock_resp(self):
        return [
            {
                "input": "NC_000001.11:g.100A>T",
                "most_severe_consequence": "missense_variant",
                "transcript_consequences": [
                    {
                        "strand": -1,
                        "hgnc_id": 26052,
                        "consequence_terms": ["downstream_gene_variant"],
                        "distance": 976,
                        "impact": "MODIFIER",
                        "biotype": "retained_intron",
                        "gene_symbol": "CPSF3L",
                        "variant_allele": "G",
                        "transcript_id": "ENST00000323275",
                        "gene_symbol_source": "HGNC",
                        "gene_id": "ENSG00000127054",
                    }
                ],
                "colocated_variants": [{"minor_allele_freq": 0.1}],
            },
            {
                "input": "NC_000001.11:g.200C>G",
                "most_severe_consequence": "missense_variant",
                "transcript_consequences": [
                    {
                        "variant_allele": "G",
                        "gene_symbol": "ACAP3",
                        "gene_id": "ENSG00000131584",
                        "gene_symbol_source": "HGNC",
                        "transcript_id": "ENST00000353662",
                        "hgnc_id": 16754,
                        "consequence_terms": ["upstream_gene_variant"],
                        "strand": -1,
                        "impact": "MODIFIER",
                        "biotype": "protein_coding",
                        "distance": 2735,
                    }
                ],
                "colocated_variants": [{"minor_allele_freq": 0.2}],
            },
        ]

    @pytest.fixture(autouse=True)
    def expected_resp(self):
        return [
            {
                "chrom": "1",
                "pos": 100,
                "ref": "A",
                "alt": "T",
                "total_coverage": 100,
                "variant_coverage": 50,
                "variant_frequency": 0.5,
                "hgvs_notation": "NC_000001.11:g.100A>T",
                "gene_symbol": "CPSF3L",
                "consequence_terms": ["downstream_gene_variant"],
                "most_severe_consequence": "missense_variant",
                "minor_allele_freq": 0.1,
                "biotype": "retained_intron",
                "transcript_id": "ENST00000323275",
                "gene_id": "ENSG00000127054",
            },
            {
                "chrom": "1",
                "pos": 200,
                "ref": "C",
                "alt": "G",
                "total_coverage": 100,
                "variant_coverage": 50,
                "variant_frequency": 0.5,
                "hgvs_notation": "NC_000001.11:g.200C>G",
                "gene_symbol": "ACAP3",
                "consequence_terms": ["upstream_gene_variant"],
                "most_severe_consequence": "missense_variant",
                "minor_allele_freq": 0.2,
                "biotype": "protein_coding",
                "transcript_id": "ENST00000353662",
                "gene_id": "ENSG00000131584",
            },
        ]

    def test_fetch_annotations(self, mock_resp, test_data, expected_resp):
        with patch("api_client.fetch_response") as mock_fetch_response:
            mock_fetch_response.return_value = mock_resp
            assert fetch_annotations(test_data) == expected_resp

    def test_fetch_annotations_empty(self, test_data):
        with patch("api_client.fetch_response") as mock_fetch_response:
            mock_fetch_response.return_value = []
            assert fetch_annotations(test_data) == []


class TestFetchResponse:
    @pytest.fixture(autouse=True)
    def test_chunks(self):
        return [{"hgvs_notation": "ABC123"}, {"hgvs_notation": "DEF456"}]

    @pytest.fixture(autouse=True)
    def expected_resp(self):
        return [
            {"hgvs_notation": "ABC123", "extra_data": "here"},
            {"hgvs_notation": "DEF456", "extra_data": "here"},
        ]

    def test_fetch_response(self, test_chunks, expected_resp):
        with patch("api_client.requests.post") as mock_post:
            mock_post.return_value.ok = True
            mock_post.return_value.json.return_value = expected_resp
            assert fetch_response(test_chunks) == expected_resp

    def test_fetch_response_not_ok(self, test_chunks):
        with patch("api_client.requests.post") as mock_post:
            mock_post.return_value.ok = False
            with pytest.raises(SystemExit):
                fetch_response(test_chunks)
