
# coding: utf-8

# In[ ]:

from itertools import repeat


# In[ ]:

def accidentally_many_spaces(text, generator=False):
    paras = text.splitlines()
    if generator:
        return accidentally_many_spaces_generator(paras)
    else:
        return accidentally_many_spaces_recursive(paras)


# In[ ]:

def accidentally_many_spaces_recursive(paras):
    r = ''
    for para in reversed(text.splitlines()):
        r = para + ' ' + ' '.join(r)
    return r


# In[ ]:

def accidentally_many_spaces_generator(paras):
    yield from paras[0]
    for i, para in enumerate(paras[1:]):
        for char in para:
            yield from repeat(' ',(2<<i)-1)
            yield char


# In[ ]:

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    generator = False
    if '-g' in args:
        args.remove('-g')
        generator = True
    try:
        in_fn, out_fn = args
    except ValueError:
        print('usage: python AccidentallyManySpaces.py in.txt out.txt [-g]')
        raise
    with open(in_fn,'r',encoding='utf-8') as in_file:
        text = in_file.read()
    with open(out_fn,'w',encoding='utf-8') as out_file:
        if generator:
            for char in accidentally_many_spaces(text, True):
                out_file.write(char)
        else:
            paras = paras = [x+' ' for x in text.splitlines()]
            out_file.write(accidentally_many_spaces_recursive(paras))

