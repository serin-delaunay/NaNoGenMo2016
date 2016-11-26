
# coding: utf-8

# In[1]:

import Questions


# In[2]:

print(Questions.questions[-1].instantiate(2))


# In[3]:

for q,(a1,a2) in sorted(Questions.question_set(Questions.questions, 15)):
    print(q)
    print('  '+a1)
    print('  '+a2)


# In[4]:

for x in [Questions.qg.flatten('#title_full_name# (#pronouns#)') for i in range(20)]:
    print(x)

