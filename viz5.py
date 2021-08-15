from requests import get, post
from rutermextract import TermExtractor
from bs4 import BeautifulSoup
from pprint import pprint
from itertools import product
from math import tanh
from time import sleep
from utilites import load, dump
from random import randint, choice
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
    useragents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; Trident/4.0;)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.112",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.1",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.6.0 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPod; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (iPad; CPU OS 11_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_5_1 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/90.0",
        "Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:90.0) Gecko/90.0 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPod touch; CPU iPhone 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 EdgA/46.6.4.5160",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/46.3.13 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edge/40.15254.603",
        "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (iPod touch; CPU iPhone 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 YaBrowser/21.6.3.883 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (Linux; arm_64; Android 11; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.3.4.59 Mobile Safari/537.36",
    ]
    def parse_dukcduckgo (term):
        print("Parsing for ", term, end='...', flush=1)
        sleep(randint(0,5))
        x = post(
    		'https://html.duckduckgo.com/html/', 
    		data={'q':term.replace(' ', '+')}, 
    		headers = {'user-agent': choice(useragents),},
            timeout=5
        ).content
        dom = BeautifulSoup(x, features="html5lib")
        try:
            open('/tmp/%s.html' % term, 'w').write(dom.prettify())
        except FileNotFoundError:
            print("FileNotFoundError", term)
        snippets = [ x.text for x in dom('a', {'class':'result__snippet'}) ]
        text = " ".join(snippets)
    
        return text
    
    try:
        result = keywords_by_keyword[term]
        assert result
    except (KeyError, AssertionError):
        text = parse_dukcduckgo(term)
        result = get_keywords(text)
        if result:
            keywords_by_keyword.update({term:result})
            dump(keywords_by_keyword, 'keywords_by_keyword.json')
        print("... ", len(result), " received")
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
	"/home/student/fff/txt/Адыгея.txt",
	"/home/student/fff/txt/Татарстан.txt",
	"/home/student/fff/txt/Алтай.txt",
	"/home/student/fff/txt/Дагестан.txt",
	"/home/student/fff/txt/Ингушетия.txt",
	"/home/student/fff/txt/Кабардино-Балкарская.txt",
	"/home/student/fff/txt/Калмыкия.txt",
	"/home/student/fff/txt/Карачаево-Черкессия.txt",
	"/home/student/fff/txt/Крым.txt",
	"/home/student/fff/txt/Тыва.txt",
	"/home/student/fff/txt/Чечня.txt",
]:
    print("Parsing ", url, end="... ")
    kw = set(get_text_keywords(url))
    print("done")
    kw_set.update({url:kw})

    for term in list(kw):
        kw = set(get_internet_keywords(term))
        kw_set.update({url:kw | kw_set[url]})

    print("Filtering keywords ", url, end="... ", flush=1)
    filtered_keywords = kw_set[url]
    # filtered_keywords = set(filter_keywords(list(kw_set[url])))
    kw_set.update({url:filtered_keywords})
    print("done")


out_table = {}
regions = [ re.findall(r'.*/(.*?)\..*', x)[0] for x in kw_set.keys() ]
for region_a in regions:
    url_a = "/home/student/fff/txt/%s.txt" % region_a
    total = len(kw_set[url_a])
    prime = ", ".join(keywords_by_url[url_a][:3])
    is_lower_part = 1
    out_table.update({region_a:{"Всего понятий":total, " Пример": prime}})
    for region_b in regions:
        if region_a != region_b:
            url_b = "/home/student/fff/txt/%s.txt" % region_b
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