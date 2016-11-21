
# coding: utf-8

# In[1]:

from Grammar import Grammar


# In[2]:

g = Grammar({
     'story':['<sentence>',
              ('<story> <sentence>',9.0)],
     'sentence': ['<noun_phrase> <verb_phrase>.'],
     'noun_phrase':['<article> <determined_noun_phrase>',
                    '<name>'],
     'article':['the','a'],
     'determined_noun_phrase':['<adjective> <determined_noun_phrase>',
                               '<noun>'],
     'adjective':['wonderful', 'terrible', 'barnacle-infested',
                  'glistening', 'second-hand','brand new'],
     'noun':['cat', 'bee', 'harpy', 'museum', 'schooner', 'postbox', 'doorbell', 'pokemon'],
     'name':['Aerith', 'Bob', 'Macavity', 'Windle Poons', 'Klaatu', 'Boo'],
     'verb_phrase':['<prep_verb_phrase> <preposition_phrase>',
                    '<prep_verb_phrase>'],
     'preposition_phrase':['near <noun_phrase>',
                           'on <noun_phrase>',
                           'with <noun_phrase>'],
     'prep_verb_phrase':['<intransitive_verb>',
                         '<transitive_verb> <noun_phrase>'],
     'intransitive_verb':['sleeps', 'complains', 'flollops', 'pontificates', 'dies', 'jokes'],
     'transitive_verb':['calls', 'convinces', 'trusts', 'licks']
    })


# In[3]:

g.generate('<story>')

