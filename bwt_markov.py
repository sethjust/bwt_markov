#!/usr/bin/env python

from bwt import BWT
from random import choice

class MarkovModel:
  def __init__(self, string):
    self.string = string
    self.bwt = BWT(self.string)

  def get_n_tokens(self, context, n):
    '''
    Returns up to n tokens that follow the list of tokens given in context in
    the source string, or None if no such tokens exist.
    '''
    indices = self.bwt.get_start_indices(context)

    if indices == []:
      return None

    index = choice(indices)
    return self.get_n_gram_at_index(n, index)

  def get_n_gram_at_index(self, n, index):
    return self.string[index+1:min(index+1+n ,len(self.string)-1)]

  def get_all_possible_n_grams(self, context, n):
    indices = self.bwt.get_start_indices(context)
    return (self.get_n_gram_at_index(n, index) for index in indices)

