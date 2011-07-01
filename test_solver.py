import unittest
import solver

class TestDictionary(unittest.TestCase):
    def test_load1(self):
        """Check the dictionary can load the right words."""
        d = solver.Dictionary('A')
        self.assertEqual(d.word_list[0], 'a')

    def test_invalidword(self):
        self.assertRaises(solver.InvalidWordException, solver.Dictionary, 'abc.def')

    def test_matching(self):
        d = solver.Dictionary('match')
        self.assertEqual(d.matching_words, ['match'])

        d = solver.Dictionary('h?t')
        self.assertEqual(len(d.matching_words) > 2, True)