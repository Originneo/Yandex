import os
import sys
import pandas as pd
import fnmatch
import json
import re

from pymystem3 import Mystem
m = Mystem()

data = []
for root, dir1, files in os.walk('../'):
    for item in fnmatch.filter(files, "*.txt"):
        data.append([root.split('/')[-1], open(os.path.join(root, item)).read()])
        
data = pd.DataFrame(data)
data.columns = ['tag', 'text']
data.text = data.text.apply(lambda x: re.sub(r'[^\w\s]', ' ', x.lower()))
data.text = data.text.apply(lambda x: re.sub('\d', ' ', x))
data.text = data.text.apply(lambda x: re.sub(r'[\n\r\t]', ' ', x))
data.text = data.text.apply(lambda x: ' '.join(re.split("[^а-я]*", x.lower())))
data.text = data.text.apply(lambda x: m.lemmatize(x))
data.text = data.text.apply(lambda x: [i for i in x if ' ' not in i])

uni = []
for i in data.text:
    uni += i
uni = sorted(list(set(uni)))

num2v = {}
v2num = {}
for i, v in enumerate(uni):
    v2num[v] = i
    num2v[i] = v
    
json.dump(num2v, open('../data/num2v.json', 'w'))
json.dump(v2num, open('../data/v2num.json', 'w'))

data.text = data.text.apply(lambda x: ' '.join(str(v2num[i]) for i in x))
data.to_csv('../data/prepared.csv', index=False)