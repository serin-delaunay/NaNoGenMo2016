
# coding: utf-8

# In[1]:

import tracery
from tracery import modifiers


# In[2]:

import inflect


# In[3]:

p = inflect.engine()


# In[4]:

def possessive(text, *params):
    return text+"'s"
modifiers.possessive = possessive
modifiers.base_english['possessive'] = possessive


# In[5]:

def s(text, *params):
    return p.plural_noun(text)
modifiers.s = s
modifiers.base_english['s'] = s


# In[6]:

def a(text, *params):
    return p.a(text)
modifiers.a = a
modifiers.base_english['a'] = a

