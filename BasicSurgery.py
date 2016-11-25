
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

from tracery import Grammar, modifiers


# In[7]:

predicates = {}


# In[8]:

skull_open = DualPredicate('open', 'closed', ('body_id',))
predicates['open'] = skull_open
predicates['closed'] = skull_open.neg()
empty = Predicate('empty', ('body_id',))
predicates['empty'] = empty
on_ice = Predicate('on_ice', ('brain_id',))
predicates['on_ice'] = on_ice
brain_in = Predicate('brain_in', ('brain_id','body_id'))
predicates['brain_in'] = brain_in


# In[9]:

open_skull = Action(
    name='open_skull',
    parameters=[('body', 'body_id')],
    preconditions=[skull_open('body_id').neg()],
    effects=[skull_open('body_id')])
predicates['open_skull'] = open_skull.predicate()


# In[10]:

close_skull = Action(
    name='close_skull',
    parameters=[('body', 'body_id')],
    preconditions=[skull_open('body_id')],
    effects=[skull_open('body_id').neg()])
predicates['close_skull'] = close_skull.predicate()


# In[11]:

remove_brain = Action(
    name='remove_brain',
    parameters=(('brain', 'brain_id'),
                ('body', 'body_id')),
    preconditions=(skull_open('body_id'),
                   brain_in('brain_id', 'body_id'),
                   on_ice('brain_id').neg(),
                   empty('body_id').neg()),
    effects=(brain_in('brain_id', 'body_id').neg(),
             empty('body_id'),
             on_ice('brain_id')))
predicates['remove_brain'] = remove_brain.predicate()


# In[12]:

replace_brain = Action(
    name='replace_brain',
    parameters=(('brain', 'brain_id'),
                ('body', 'body_id')),
    preconditions=(skull_open('body_id'),
                   brain_in('brain_id', 'body_id').neg(),
                   on_ice('brain_id'),
                   empty('body_id')),
    effects=(brain_in('brain_id', 'body_id'),
             empty('body_id').neg(),
             on_ice('brain_id').neg()))
predicates['replace_brain'] = replace_brain.predicate()


# In[13]:

brain_surgery = pyddl.Domain(actions=(open_skull,
                                      close_skull,
                                      remove_brain,
                                      replace_brain))


# In[14]:

init_state = [brain_in('2','2'),
              brain_in('1','1'),
              skull_open('1').neg(),
              skull_open('2').neg()]
goal_state=[brain_in('1','2'),
            brain_in('2','1'),
            skull_open('1').neg(),
            skull_open('2').neg()]
subject_ids = ('1', '2')
objects={'brain': subject_ids,
         'body': subject_ids}


# In[15]:

two_brain_swap = Problem(domain=brain_surgery,
                         objects=objects,
                         init=init_state,
                         goal=goal_state)


# In[16]:

def brain_surgery_heuristic(state):
    r = 0.0
    for p in state.predicates:
        if(p[0] == 'open'):
            r += 0.0#0.1
        elif(p[0] == 'on_ice'):
            r += 0.4
        elif(p[0] == 'empty'):
            r += 0.4
    return r


# In[17]:

#tbs_plan = pyddl.planner(two_brain_swap, heuristic=brain_surgery_heuristic)
tbs_plan = pyddl.planner(two_brain_swap)


# In[18]:

for action in tbs_plan:
    print(action)


# In[19]:

def possessive(text, *params):
    return text+"'s"
modifiers.base_english['possessive'] = possessive


# In[20]:

g = Grammar({
        'open':'#body_id.possessive# cranium is open and the brain is exposed',
        'closed':'#body_id.possessive# cranium is either intact, or closed and repaired',
        'brain_in':'#brain_id.possessive# brain is in #body_id.possessive# head',
        'empty':'#body_id.possessive# head does not contain a brain',
        'on_ice':'#body_id.possessive# brain is stored in an ice box',
        'open_skull':'open #body_id.possessive# skull carefully using a chainsaw',
        'close_skull':'replace the removed section of #body_id.possessive# skull with a sterilised metal plate and suture the skin',
        'remove_brain':'disconnect #brain_id.possessive# brain from peripheral nervous system connections and remove it from #body_id.possessive# skull',
        'replace_brain':'apply nerve growth factor to connection sites in #body_id.possessive# empty skull and #brain_id.possessive# brain, then place #brain_id.possessive# brain in #body_id.possessive# body'
    })
g.add_modifiers(modifiers.base_english)


# In[21]:

for i, subject_id in enumerate(subject_ids):
    g.push_rules(subject_id,'subject {0}'.format(chr(ord('A')+int(i))))


# In[22]:

for condition in init_state:
    print(condition.flatten(g))
print()
for action in tbs_plan:
    print(predicates[action.name](*action.sig[1:]).flatten(g))
print()
for condition in goal_state:
    print(condition.flatten(g))

