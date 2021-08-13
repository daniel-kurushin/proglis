from requests import get, post
from rutermextract import TermExtractor
from bs4 import BeautifulSoup
from pprint import pprint
from itertools import product
from math import tanh
from time import sleep
from utilites import load, dump

import re

try:
    keywords_by_url = load('keywords_by_url.json')
except FileNotFoundError:
    keywords_by_url = {}

try:
    keywords_by_keyword = load('keywords_by_keyword.json')
except FileNotFoundError:
    keywords_by_keyword = {}

te = TermExtractor()

stopterms = ['англ', 'такой образ', 'российская федерация', 'дата сохранения', 'надёжная правовая поддержка www.consultant.ru', 'создание условий', 'вид деятельности']
stopwords = ['республик']

def dict_to_xls(filename = '/tmp/out.xls', IN = {}):
    
    import xlwt
    wb = xlwt.Workbook(encoding = 'UTF-8')
    ws = wb.add_sheet('Sheet 1')
    i = 1
    for key1 in IN.keys():
        ws.write(i, 0, key1)
        j = 1
        for key2 in IN[key1].keys():
            ws.write(i, j, IN[key1][key2])
            j += 1
        i += 1
    j = 1
    for key2 in IN[key1].keys():
        ws.write(0, j, key2)
        j += 1

    wb.save(filename)

def get_keywords(text):
    result = [
    		t.normalized for t in te(text) if t.normalized.count(' ') > 0 and 
                                        t.normalized not in stopterms and 
                                        sum([ sw in t.normalized for sw in stopwords ]) == 0 and
                                        re.match(r'[а-я]', t.normalized) and 
                                        not re.match(r'[0-9]', t.normalized) and 
                                        not re.match(r'[a-z]', t.normalized) and 
                                        t.count > 1
    ]
    return result

def get_internet_keywords(term):

    def parse_dukcduckgo (term):
        sleep (2)
        x = post(
    		'https://html.duckduckgo.com/html/', 
    		data={'q':term.replace(' ', '+')}, 
    		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
        ).content
        dom = BeautifulSoup(x, features="html5lib")
        snippets = [ x.text for x in dom('a', {'class':'result__snippet'}) ]
        text = " ".join(snippets)
    
        return text
    
    try:
        result = keywords_by_keyword[term]
        assert result
    except (KeyError, AssertionError):
        text = parse_dukcduckgo(term)
        result = get_keywords(text)
        keywords_by_keyword.update({term:result})
        dump(keywords_by_keyword, 'keywords_by_keyword.json')
    return result

def get_text_keywords(url):
    text = open(url).read()
    try:
        keywords = keywords_by_url[url]
        assert keywords
    except (KeyError, AssertionError):
        keywords = get_keywords(text)
        keywords_by_url.update({url:keywords})
        dump(keywords_by_url, 'keywords_by_url.json')
    
    return keywords

def compare(S1,S2):
    ngrams = [S1[i:i+3] for i in range(len(S1))]
    count = 0
    for ngram in ngrams:
        count += S2.count(ngram)

    return count/max(len(S1), len(S2))

def compare_phrase(P1, P2):
    def func(x, a=0.00093168, b=-0.04015416, c=0.53029845):
        return a * x ** 2 + b * x ** 1 + c 
    
    P1 = P1.lower().split() if type(P1) == str else [ x.lower() for x in P1 ]
    P2 = P2.lower().split() if type(P2) == str else [ x.lower() for x in P2 ]
    n, v = 0, 0
    for a, b in set([ tuple(sorted((a, b))) for a, b in product(P1, P2)]):
        v += compare(a,b)
        n += 1
    try:
        return tanh((v / n) / func(max(len(P1),len(P2))))
    except ZeroDivisionError:
        return 0       
   
def filter_keywords (keywords):
    try:
        rez = [keywords[0]]
        for kw in keywords:
            tmp = []
            for a,b in set([ tuple(sorted((a, b))) for a, b in product(rez, [kw])]):
                v = compare_phrase(a,b)
                tmp += [(v, a)]        
                w = sorted(tmp, reverse=1)[0][0]
            if w < 0.5:
                rez += [kw]
        return rez
    except IndexError:
        return []
     
term_list = []
pair_list = []

kw_set = {} 
for url in [
	"/home/dan/src/proglis/txt/Адыгея.txt",
	"/home/dan/src/proglis/txt/Татарстан.txt",
	"/home/dan/src/proglis/txt/Алтай.txt",
	"/home/dan/src/proglis/txt/Дагестан.txt",
	"/home/dan/src/proglis/txt/Ингушетия.txt",
	"/home/dan/src/proglis/txt/Кабардино-Балкарская.txt",
	"/home/dan/src/proglis/txt/Калмыкия.txt",
	"/home/dan/src/proglis/txt/Карачаево-Черкессия.txt",
	"/home/dan/src/proglis/txt/Крым.txt",
	"/home/dan/src/proglis/txt/Тыва.txt",
	"/home/dan/src/proglis/txt/Чечня.txt",
]:
    kw = set(get_text_keywords(url))
    kw_set.update({url:kw})
#    term_list = filter_keywords(kw)
#    kw = term_list
    for term in list(kw)[0:1]:
        kw = set(get_internet_keywords(term))
        kw_set.update({url:kw | kw_set[url]})
#        kw_for_kw = get_text_keywords(text)
##        filtered_kw_for_kw = filter_keywords(kw_for_kw)
#        filtered_kw_for_kw = kw_for_kw
#        term_list += filtered_kw_for_kw
#        pair_list += [ (term, x) for x in filtered_kw_for_kw ]

#open_graph('big-graph.dot')
#for a,b in pair_list:
#    write_graph('big-graph.dot', a, b)
#close_graph('big-graph.dot')

out_table = {}
regions = [ re.findall(r'.*/(.*?)\..*', x)[0] for x in kw_set.keys() ]
for region_a in regions:
    url_a = "/home/dan/src/proglis/txt/%s.txt" % region_a
    total = len(kw_set[url_a])
    prime = ", ".join(keywords_by_url[url_a][:3])
    is_lower_part = 1
    out_table.update({region_a:{"Всего понятий":total, " Пример": prime}})
    for region_b in regions:
        if region_a != region_b:
            url_b = "/home/dan/src/proglis/txt/%s.txt" % region_b
            both = kw_set[url_a] & kw_set[url_b]
            b_only = kw_set[url_b] - kw_set[url_a]
            a_only = kw_set[url_a] - kw_set[url_b]
            if is_lower_part:
                out_table[region_a].update({region_b:len(both)})
            else:
                out_table[region_a].update({region_b:len(b_only)})
        else:
            is_lower_part = 0
            out_table[region_a].update({region_b:"X"})

dict_to_xls(IN=out_table)