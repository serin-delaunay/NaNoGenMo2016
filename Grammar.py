
# coding: utf-8

# In[1]:

import re
from itertools import accumulate
from collections import namedtuple
import random


# In[2]:

Token = namedtuple("Token", ["text", "is_nonterminal"])
Option = namedtuple("Option", ["tokens", "weight"])
Node = namedtuple("Node", ["nonterminal", "text"])


# In[3]:

class Production:
    def __init__(self, prods):
        self.options = []
        if isinstance(prods, list):
            for prod in prods:
                self.options.append(self.make_option(prod))
        else:
            self.options.append(self.make_option(prods))
    @classmethod
    def make_option(cls, prod):
        if isinstance(prod, tuple):
            s, weight = prod
        else:
            s, weight = prod, 1.0
        return Option(cls.parse_option(s), weight)
    @classmethod
    def parse_option(cls, option):
        pattern = "(?<!\\\\)<[\w]+>"
        nonterminals = re.findall(pattern, option)
        terminals = re.split(pattern, option)
        r = []
        for t, nt in zip(terminals, nonterminals):
            if(t != ''):
                r.append(Token(t, False))
            r.append(Token(nt[1:-1], True))
        t = terminals[-1]
        if(t != ''):
            r.append(Token(t, False))
        return r
    def __repr__(self):
        return '\n'.join(["{0}: ".format(option.weight) +
                          ''.join(['<{0}>'.format(x.text) if x.is_nonterminal else x.text
                                   for x in option.tokens])
                          for option in self.options])
    def expand_nonterminal(self, grammar, nonterminal, tree=False):
        text = grammar[nonterminal.text].generate(grammar, tree)
        if tree:
            return Node(nonterminal.text, text)
        else:
            return text
    def generate(self, grammar, tree=False):
        if len(self.options) > 1:
            total_weight = sum(o.weight for o in self.options)
            r = random.random()*total_weight
            for o, x in zip(self.options, accumulate(o.weight for o in self.options)):
                if x > r:
                    option = o
                    break
        else:
            option = self.options[0]
        output = (self.expand_nonterminal(grammar, x, tree)
                  if x.is_nonterminal else x.text
                  for x in option.tokens)
        if tree:
            return list(output)
        else:
            return ''.join(output)


# In[4]:

def grammify(*args):
    d = {}
    for g in args:
        for (k,v) in g.items():
            d[k] = Production(v)
    return d


# In[5]:

def generate_tree(start, *args):
    return Production(start).generate(grammify(*args), True)


# In[6]:

class Grammar:
    def __init__(self, *args):
        self._data = {}
        for g in args:
            self.add_entries(g)
    def add_entries(self, g):
        for (k,v) in g.items():
            self._data[k] = Production(v)
    def __getitem__(self, k):
        return self._data[k]
    def generate(self, start, tree=False):
        return Production(start).generate(self, tree)

