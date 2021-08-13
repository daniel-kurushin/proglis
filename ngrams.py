from glob import glob
from nltk.tokenize import WordPunctTokenizer as WPT
from utilites import dump, compare

import re 

wpt = WPT()

words = []
for txt in glob('txt/*'):
    words += [ x for x in wpt.tokenize(open(txt).read()) if len(x) > 3 and not re.findall(r'\d+|[a-z]+|\W+|_+', x) ]

ngrams = {} 

for n in [2,3,4,5]:
    for i in range(len(words)):
        x = words[i:n+i]
        if len(set(x)) == n:
            ngram = " ".join(x) 
        try:
            ngrams[ngram] += 1
        except KeyError:
            ngrams.update({ngram:1})
            
ngrams = sorted(( x for x in ngrams.items() if x[1] > 2 ), key=lambda x: x[1])

dump(ngrams, 'ngrams.json')