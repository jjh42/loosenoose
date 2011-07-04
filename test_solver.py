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

    def test_guess(self):
        d = solver.Dictionary('guess')
        self.assertEqual(d.predictions, [])

        d = solver.Dictionary('t?st')
        self.assertEqual(d.predictions[0][0], 'e')

        d = solver.Dictionary('?ueen')
        self.assertEqual(d.predictions[0][0], 'q')

    def test_empty(self):
        d = solver.Dictionary('?')
        self.assertEqual(d.predictions[0][1], 1./26.)
        d = solver.Dictionary('??')
        d = solver.Dictionary('???')
