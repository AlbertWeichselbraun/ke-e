#!/usr/bin/env python

from urllib.request import urlopen
from pickle import dump, load

#with urlopen('https://www.fhgr.ch') as f:
#    content = f.read().decode('utf8')
#
#    with open('save.obj', 'wb') as g:
#        dump(content, g)

with open('save.obj', 'rb') as f:
    content = load(f)
    print(content)
