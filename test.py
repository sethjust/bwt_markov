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
    bwt.print_table()
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
    markov = MarkovModel(list("blah blah blah blah blah blah baabab blah blah"))

    results = {'a': 0, 'b': 0}

    for i in range(1000):
      token = markov.get_n_tokens(list("ba"), 1)[0]
      results[token] += 1

    log_ratio = self.log_ratio(results, 'a', 'b')
    print "BWT: log ratio is", log_ratio
    self.assertTrue(abs(log_ratio) < .15) # close enough -- between .86 and 1.16 (e^-0.15, e^0.15)

#    results = {'a': 0, 'b': 0}
#    for i in range(1000):
#      pass


  def log_ratio(self, results, a, b):
    log_ratio = math.log(results[a]/float(results[b]))
    return log_ratio

