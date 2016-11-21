
# coding: utf-8

# In[1]:

import pyddl


# In[2]:

from collections import namedtuple


# In[3]:

# possible things to add:
# disjunctive goals
# disjunctive action preconditions


# In[4]:

class Predicate(namedtuple('Predicate',
                ['name'])):
    def __call__(self, *args):
        return GroundedPredicate(self, args)
    def condition(self, *args):
        return ((self.name,)+tuple(args),)
    def effect(self, *args):
        return ((self.name,)+tuple(args),)
    def neg(self):
        return NegativePredicate(self.name)


# In[5]:

class NegativePredicate(namedtuple('NegativePredicate',
                                   ['name'])):
    def __call__(self, *args):
        return GroundedPredicate(self, args)
    def condition(self, *args):
        return ()
    def effect(self, *args):
        return (pyddl.neg(self.neg().effect(*args)[0]),)
    def neg(self):
        return Predicate(self.name)


# In[6]:

class DualPredicate(namedtuple('DualPredicate',
                               ['name', 'negative_name'])):
    def __call__(self, *args):
        return GroundedPredicate(self, args)
    def condition(self, *args):
        return ((self.name,)+tuple(args),)
    def effect(self, *args):
        return (self.condition(*args)[0], pyddl.neg(self.neg().condition(*args)[0]))
    def neg(self):
        return DualPredicate(self.negative_name, self.name)


# In[7]:

class GroundedPredicate(namedtuple('GroundedPredicate',
                                 ['predicate', 'parameters'])):
    def condition(self):
        return self.predicate.condition(*self.parameters)
    def effect(self):
        return self.predicate.effect(*self.parameters)
    def neg(self):
        return GroundedPredicate(self.predicate.neg(), self.parameters)


# In[8]:

def Action(name, parameters=(), preconditions=(), effects=(),
           unique=False, no_permute=False):
    return pyddl.Action(name=name,
                        parameters=tuple(parameters),
                        preconditions=sum((p.condition() for p in preconditions), ()),
                        effects=sum((e.effect() for e in effects), ()),
                        unique=unique, no_permute=no_permute)


# In[9]:

def Problem(domain, objects, init=(), goal=()):
    return pyddl.Problem(domain=domain,
                         objects=objects,
                         init=sum((i.condition() for i in init), ()),
                         goal=sum((g.condition() for g in goal), ()))

