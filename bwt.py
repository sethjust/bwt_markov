#!/usr/bin/env python

from collections import deque

class BWT:
  END = "__END__SYMBOL__"

  def __init__(self, symbols):
    '''
    symbols should be a list of tokens that will be treated as atoms.
    '''
    self.deq = deque(symbols)
    self.deq.append(self.END)

    # This method simply builds a table, which is only suitable for small
    # strings
    self.build_rotations()
    self.sort_table()

    # Now build the functions we need to compute sequence matches
    self.build_functions()

  def build_rotations(self):
    self.table = []
    for i in range(len(self.deq)):
      self.table.append([])
      for j in range(len(self.deq)):
        # This is going to be slow -- accessing the middle of the deque is O(n)
        self.table[i].append(self.deq[-j])
      self.deq.rotate(-1)

  def sort_table(self):
    table_and_prefix = [(self.table[i], i) for i in range(len(self.table))]
    sorted_table_and_prefix = sorted(table_and_prefix, key=lambda (a, b): a , cmp=TableSorter())
    self.table = [a for a,b in sorted_table_and_prefix]
    self.prefix = [b for a,b in sorted_table_and_prefix]

  def transform(self):
    col = []
    for i in range(len(self.table)):
      col.append(self.table[i][-1])
    return col

  def build_functions(self):
    col = self.transform()

    counts = {}
    running_counts = []
    for token in col:
      running_counts.append(counts.copy())

      # Store counts for each token
      if token in counts.keys():
        counts[token] += 1
      else:
        counts[token] = 1
    running_counts.append(counts)

    tokens = sorted(counts.keys(), cmp=TokenSorter())
    lookup = {}
    count = 0
    for token in tokens:
      lookup[token] = count
      count += counts[token]
    self.C = CFunction(lookup)
    self.F = FFunction(running_counts)

  def L(self, W):
    '''
    W is a list of tokens -- only random access and slicing is used.

    Returns 1-indexed locations.
    '''
    if len(W) == 0:
      return 1
    return self.C(W[0]) + self.F(W[0], self.L(W[1:]) - 1) + 1
  
  def U(self, W):
    '''
    W is a list of tokens -- only random access and slicing is used.

    Returns 1-indexed locations.
    '''
    if len(W) == 0:
      return len(self.table)
    return self.C(W[0]) + self.F(W[0], self.U(W[1:]))

  def get_start_indices(self, W):
    '''
    Returns the indices in the original symbol string at which W occurs.
    '''
    W = W[::-1] # Need to adjust for searching being backwards
    return self.convert_to_index(self.L(W), self.U(W))

  def convert_to_index(self, l, u):
    # To convert a 1-indexed (inclusive range) into a 0-indexed left-inclusive
    # (python-style) range, just subtract one from the left-hand index.
    return [self.prefix[row] for row in range(l - 1, u)]

  def print_table(self):
    i = 0
    for row in self.table:
      i += 1
      print i, '(', self.prefix[i-1], ')', row
    print

class CFunction:
  def __init__(self, lookup):
    self.lookup = lookup
  
  def __call__(self, x):
    try:
      return self.lookup[x]
    except:
      return 0

class FFunction:
  def __init__(self, running_counts):
    self.running_counts = running_counts

  def __call__(self, x, i):
    try:
      res = self.running_counts[i][x]
      if res == None:
        return 0
      else:
        return res
    except:
      return 0

class TableSorter:
  def __init__(self):
    self.token_sorter = TokenSorter()

  def __call__(self, a, b):
    for i in range(min(len(a), len(b))):
      res = self.token_sorter(a[i], b[i])
      if res != 0:
        return res
    return cmp(len(a), len(b))

class TokenSorter:
  def __call__(self, a, b):
    if str(a) == str(b):
      return 0
    elif a == BWT.END:
      return -1
    elif b == BWT.END:
      return 1
    elif str(a) < str(b):
      return -1
    elif str(a) > str(b):
      return 1
    else:
      return 0
