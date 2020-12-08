from glob import glob
from rutermextract import TermExtractor as TE
from utilites import dump
import re

te = TE()

_out = {}
for txt in glob('txt/*'):
    reg = re.findall(r'.*/(.*)\..*', txt)[0]
    terms = te(open(txt).read(), strings=1)
    _out.update({reg:terms})

dump(_out, 'out.json')