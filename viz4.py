from glob import glob
from rutermextract import TermExtractor as TE
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import SpaceTokenizer as ST
from pymorphy2 import MorphAnalyzer
from utilites import load, dump, compare, compare_phrase
from math import exp, pow
from bs4 import BeautifulSoup as BS
from requests import get

import re

ngrams = load('ngrams.json')
to_upper_list = ['ВВП', 'ЕГЭ', 'РФ', 'ОАО', 'АПК', 'ВСТО', 'ВТО', 'ЦФО','СЗФО','ЮФО','СКФО','ПФО','УрФО','СФО','ДФО','ДВФО',]

ma = MorphAnalyzer()
pst = PST()
st = ST()
term_extractor = TE()

def k(t):
    return t.count * pow(len(st.tokenize(t.normalized)),2)
    
def norm(x):
    return pow(x, 1/2)
        
def term_normal_form(term):
    _in = term.normalized
    if _in.count(' ') == 0:
        if _in.upper() in to_upper_list:
            return _in.upper() 
        elif len(set(list(_in.upper()))) == 1:
            return 'test'
        else:
            out = ''
            for variant in ma.parse(_in):
                if 'Geox' not in variant.tag and \
                   'Name' not in variant.tag:
                   out = variant
                  
            if not out:
                out = ma.parse(_in)[0]
            return out.normal_form.capitalize()
    else:
        rez = []
        for ngram, count in ngrams:
            last = ngram.split()[-1]
            w = 1
            for var in ma.parse(last):
                if var.normal_form == var:
                    w = 1.1
                    break
            k = compare_phrase(ngram, str(term)) * w
            rez += [(k, ngram)]
        
        k, out = sorted(rez, key=lambda x: x[0])[-1]
        print(out, '|', str(term), '|', k)
        if k > 0:
            return out[0].upper() + out[1:]
        else:
            return 'test'


for txt in glob('txt/*'):
    reg = re.findall(r'.*/(.*)\..*', txt)[0]
    sentences = [ x for x in pst.tokenize(open(txt).read()) if len(x) > 3 ]
    terms = {}
    for sentence in sentences:
        for term in ( (term_normal_form(t), k(t)) for t in term_extractor(sentence) if t.count > 1 and not re.findall(r'\d+|[a-z]+', t.normalized) ):
            try:
                a = terms[term[0]]
                terms[term[0]] += term[1]
                print('inc', term, a, terms[term[0]])
            except KeyError as e:
                print('upd', term)
                terms.update({term[0]:term[1]})
    
    sorted_terms = sorted(terms.items(), key=lambda x: x[1], reverse=1)
    with open("%s.dot" % reg, 'w') as graph:
        graph.write("digraph g {\n")	
        graph.write("\toverlap = false;\n");
        graph.write("\tsep=-0.8;\n");
        for word, weight in sorted_terms:
            if word != 'test':
                graph.write('\t"%s" [shape = none, fontsize = %s, fontname=\"sans\"]\n' % (word, norm(weight)));
        n0 = sorted_terms[0][0]
        for word, weight in sorted_terms:
            if word != 'test':
                graph.write('\t"%s" -> "%s" [style=invis, len=%s]\n' % (n0, word, 1/norm(weight)))
        graph.write("}\n")
