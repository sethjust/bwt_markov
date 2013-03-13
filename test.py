#!/usr/bin/env python

import math
from unittest import TestCase
from random import randrange

from bwt import BWT

from bwt_markov import MarkovModel

class BWTTest(TestCase):
  def test_list_built(self):
    bwt = BWT([1, 2])

    self.assertEqual(bwt.table[0], [BWT.END, 2, 1])
    self.assertEqual(bwt.transform(), [1, 2, BWT.END])
    self.assertEqual(bwt.C(1), 1) # There is one 1 in the string
    self.assertEqual(bwt.F(1, 1), 1) # There is one 1 in the last one characters
 
  def test_alignment(self):
    bwt = BWT(list("banana"))
#    bwt.print_table()
    string = "ana" # This can be a string, because it supports random access and slicing.

    self.assertEqual(bwt.L(string), 3)
    self.assertEqual(bwt.U(string), 4)
    self.assertEqual(sorted(bwt.get_start_indices(string)), [3,5]) # return is index of last token in match

class MarkovText(TestCase):
  def test_markov(self):
    markov = MarkovModel(list("Tom Tucker"))
    exp_tok = [["o"], ["u"]]

    token = markov.get_n_tokens(list("T"), 1)
    self.assertIn(token, exp_tok)

    tokens = [token for token in markov.get_all_possible_n_grams(list("T"), 1)]
    self.assertEqual(tokens, exp_tok)

  def test_banana(self):
    string = "blah blah blah blah blah blah baabab blah blah"
    markov = MarkovModel(list(string))

    results = {'a': 0, 'b': 0}

    for i in range(1000):
      token = markov.get_n_tokens(list("ba"), 1)[0]
      results[token] += 1

    bwt_log_ratio = self.log_ratio(results, 'a', 'b')
    print "BWT: log ratio is", bwt_log_ratio

    results = {'a': 0, 'b': 0}
    for i in range(1000):
      start = randrange(len(string))
      substring = None
      while (substring != "ba"):
        substring = string[start:start+2] if start < (len(string) - 2) else (string[-1:]+string[:1] if start == len(string) - 1 else string[-2:]+string[:0])
        start = (start + 1) % len(string)
      token = string[start+1]
      results[token] += 1

    plain_log_ratio = self.log_ratio(results, 'a', 'b')
    print "PLAIN: log ratio is", plain_log_ratio

    self.assertTrue(abs(bwt_log_ratio)<abs(plain_log_ratio))

  def log_ratio(self, results, a, b):
    log_ratio = math.log(results[a]/float(results[b]))
    return log_ratio

