import unittest

from util import chunks, create_hgvs_notation, get_maf


class TestHGVSNotation(unittest.TestCase):
    def setUp(self):
        self.chrom = "1"
        self.prefix = "c"
        self.pos = 123456
        self.ref = "A"
        self.alt = "T"
        self.expected_hgvs = "1:c.123456A>T"

    def test_hgvs_notation(self):
        hgvs = create_hgvs_notation(
            self.chrom, self.pos, self.ref, self.alt, self.prefix
        )
        self.assertEqual(hgvs, self.expected_hgvs)

    def test_hgvs_with_default_prefix(self):
        hgvs = create_hgvs_notation(self.chrom, self.pos, self.ref, self.alt)
        self.assertEqual(hgvs, "1:g.123456A>T")


class TestMAF(unittest.TestCase):
    def setUp(self):
        self.variant = {
            "colocated_variants": [
                {"some other trait": "foo"},
                {"minor_allele_freq": 0.1},
            ]
        }

    def test_maf(self):
        maf = get_maf(self.variant)
        self.assertEqual(maf, 0.1)

    def test_no_maf(self):
        variant = {}
        maf = get_maf(variant)
        self.assertEqual(maf, "Not found")

    def test_maf_not_found(self):
        variant = {"colocated_variants": [{"foo": "bar"}]}
        maf = get_maf(variant)
        self.assertEqual(maf, "Not found")


class TestChunks(unittest.TestCase):
    def setUp(self):
        self.lst = [1, 2, 3, 4, 5, 6]

    def test_chunks(self):
        n = 2
        expected = [[1, 2], [3, 4], [5, 6]]
        actual_chunks = chunks(self.lst, n)
        self.assertEqual(list(actual_chunks), expected)

    def test_chunks_with_remainder(self):
        n = 4
        expected = [[1, 2, 3, 4], [5, 6]]
        actual_chunks = chunks(self.lst, n)
        self.assertEqual(list(actual_chunks), expected)

    def test_chunks_with_empty_list(self):
        lst = []
        n = 2
        expected = []
        actual_chunks = chunks(lst, n)
        self.assertEqual(list(actual_chunks), expected)
