
# coding: utf-8

# In[1]:

import random
import re
import itertools
import os
from os import path


# In[2]:

def tokenise_text(text):
    pattern = '[\w]+'
    punctuation = re.split(pattern, text)
    words = re.findall(pattern, text)
    if len(words) == 0:
        tokens = punctuation
    else:
        tokens = list(itertools.chain.from_iterable(zip(punctuation, words)))+[punctuation[-1]]
    tokens = [x for x in tokens if x != '']
    return tokens


# In[3]:

def process_text(text, model, ngram_lengths=list(range(2,6))):
    tokens = tokenise_text(text.lower())
    for ngram_length in ngram_lengths:
        for i in range(len(tokens)-ngram_length+1):
            ngram = tokens[i:i+ngram_length]
            head, tail = tuple(ngram[:-1]),ngram[-1]
            try:
                model[head].add(tail)
            except KeyError:
                model[head] = {tail}


# In[4]:

def disable_production(rule, production):
    rule.remove(production)


# In[5]:

def capitalise(text):
    text = re.sub('\\bi\\b','I',text)
    punctuation_pattern = '[\.\?\!]+'
    alpha_pattern = '[a-zA-ZþÞȝȜ]'
    matches = [0]+[x.end() for x in re.finditer(punctuation_pattern,text)]
    if matches == [0]:
        return text.capitalize()
    matches = [matches[i:i+2] for i in range(len(matches)-1)]
    sentences = [text[a:b] for (a,b) in matches]
    starts = []
    for sentence in sentences:
        try:
            starts.append(next(re.finditer(alpha_pattern,sentence)).start())
        except StopIteration:
            starts.append(0)
    sentences = [sentence[:start]+sentence[start:].capitalize()
                 for (sentence, start) in zip(sentences, starts)]
    return ''.join(sentences)


# In[6]:

def enable_all(model):
    for rule in model.values():
        disabled_productions = [production for production in rule if not is_enabled(production)]
        for dp in disabled_productions:
            rule.difference_update(dp)
            rule.update([enabled_production(dp) for dp in disabled_productions])


# In[ ]:

def output_text(model, stop_length=50000, ngram_lengths=list(range(2,6))):
    tokens = []
    length = 0
    possibilities = list(itertools.chain.from_iterable(model.values()))
    print('output_text(): found {0} possible starting tokens'.format(len(possibilities)))
    if(len(possibilities)) == 0:
        return '',stop_length+1
    tokens.append(random.choice(possibilities))
    if(tokens[-1].isalnum()):
        length += 1
    while length <= stop_length:
        most_recent_ngrams = [tuple(tokens[-ngl:]) for ngl in ngram_lengths[::-1]]
        found_ngram = False
        for ngram in most_recent_ngrams:
            try:
                rule = model[ngram]
            except KeyError:
                continue
            possibilities = list(rule)
            if len(possibilities) == 0:
                del model[ngram]
                continue
            production = random.choice(possibilities)
            tokens.append(production)
            if random.random() < 0.9:
                rule.remove(production)
                if len(rule) == 0:
                    del model[ngram]
            if(tokens[-1].isalnum()):
                length += 1
            found_ngram = True
            break
        if not found_ngram:
            #print("Couldn't find any productions at all, stopping")
            break
    punctuation = ['.','!','?',',',';',':']
    if tokens[-1][-1] not in punctuation:
        tokens.append(random.choice(punctuation))
    #enable_all(model)
    return capitalise(''.join(tokens)), length


# In[ ]:

model = {}
corpora_dir = 'sources'
for fn in [path.join(corpora_dir,fn) for fn in os.listdir(corpora_dir)]:
    print('Processing {0}...'.format(fn))
    with open(fn,'r',encoding='utf-8') as f:
        try:
            process_text(f.read(),model)
        except UnicodeDecodeError:
            print(fn)
            raise


# In[ ]:

print('Generating and outputting story...')
chapters = []
total_length = 0
cnum = 0
with open('output/markov.txt','w',encoding='utf-8') as f:
    while total_length <= 50000:
        cnum += 1
        print('Generating chapter ({0} words to go)...'.format(50000-total_length))
        chapter, length = output_text(model,50000-total_length)
        chapters.append(chapter)
        total_length += length
        f.write('\n\n   ---   Chapter {0}   ---   \n\n'.format(cnum))
        f.write(chapter)
print('Done!')

