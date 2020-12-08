from glob import glob
from rutermextract import TermExtractor as TE
from nltk.tokenize import WordPunctTokenizer as WPT
from utilites import dump, compare
import re

wpt = WPT()

def uwords(words): 
    rez = [] 
    for w0 in words: 
        s = [0] 
        for w1 in rez: 
            s += [compare(w0, w1) > 0.6] 
        if max(s) == 0: 
            rez += [w0] 
    return rez 



with open('words.csv', 'w') as words:
    for txt in glob('txt/*'):
        reg = re.findall(r'.*/(.*)\..*', txt)[0]
        w1 = [ x.lower() for x in wpt.tokenize(open(txt).read()) if len(x) > 3 ] 
        w2 = list(set(w1))
        w3 = uwords(w2)
        print(w3)
        break
        words.write('"%s"; %s; %s; %s\n' % (reg, len(w1), len(w2), len(w3)) )

    
