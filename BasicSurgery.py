
# coding: utf-8

# In[1]:

get_ipython().magic('load_ext autoreload')


# In[2]:

get_ipython().magic('aimport Planner')


# In[3]:

get_ipython().magic('autoreload')


# In[4]:

import pyddl


# In[5]:

from Planner import Predicate, DualPredicate, Action, Problem


# In[6]:

skull_open = DualPredicate('open', 'closed')
empty = Predicate('empty')
on_ice = Predicate('on_ice')
brain_in = Predicate('brain_in')


# In[7]:

open_skull = Action(name='open_skull',
                    parameters=[('body', 'b')],
                    preconditions=[skull_open('b').neg()],
                    effects=[skull_open('b')])


# In[8]:

close_skull = Action(name='close_skull',
                    parameters=[('body', 'b')],
                    preconditions=[skull_open('b')],
                    effects=[skull_open('b').neg()])


# In[9]:

remove_brain = Action(name='remove_brain',
                      parameters=(('brain', 'b'),
                                  ('body', 'from')),
                      preconditions=(skull_open('from'),
                                     brain_in('b', 'from'),
                                     on_ice('b').neg(),
                                     empty('from').neg()),
                      effects=(brain_in('b', 'from').neg(),
                               empty('from'),
                               on_ice('b')))


# In[10]:

replace_brain = Action(name='replace_brain',
                      parameters=(('brain', 'b'),
                                  ('body', 'from')),
                      preconditions=(skull_open('from'),
                                     brain_in('b', 'from').neg(),
                                     on_ice('b'),
                                     empty('from')),
                      effects=(brain_in('b', 'from'),
                               empty('from').neg(),
                               on_ice('b').neg()))


# In[11]:

brain_surgery = pyddl.Domain(actions=(open_skull,
                                      close_skull,
                                      remove_brain,
                                      replace_brain))


# In[12]:

two_brain_swap = Problem(domain=brain_surgery,
                         objects={'brain': (1, 2),
                                  'body': (1, 2)},
                         init=[brain_in(2,2),
                               brain_in(1,1),
                               skull_open(1).neg(),
                               skull_open(2).neg()],
                         goal=[brain_in(1,2),
                               brain_in(2,1),
                               skull_open(1).neg(),
                               skull_open(2).neg()])


# In[13]:

tbs_plan = pyddl.planner(two_brain_swap)


# In[14]:

for action in tbs_plan:
    print(action)

