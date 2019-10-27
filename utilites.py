from sys import stderr
from json import  load as jload
from numpy import load as nload
from json import  dump as jdump
from numpy import save as ndump


def load(filename):
    filetype = filename.split('.')[-1]
    try:
        rez = None
        print('Loading %s ...' % filename, end = '', file = stderr)
        if filetype == 'json':
            rez = jload(open(filename))
        elif filetype == 'dat':
            rez = nload(open(filename, 'rb'))
        print(' done', file = stderr)
        return rez
    except Exception as e:
        print(' error! %s' % e, file = stderr)
        raise e
    
def dump(object, filename, quiet = 0):
    filetype = filename.split('.')[-1]
    if not quiet: print('Saving %s ...' % filename, end = '', file = stderr)
    if filetype == 'json':
        jdump(object, open(filename, 'w'), indent = 2, ensure_ascii = 0)
    elif filetype == 'dat':
        ndump(open(filename, 'wb'), object)
        if not quiet: print('done', file = stderr)

def compare(S1,S2):
    ngrams = [S1[i:i+3] for i in range(len(S1))]
    count = 0
    for ngram in ngrams:
        count += S2.count(ngram)

    return count/max(len(S1), len(S2))

if __name__ == "__main__":
    print(compare('привет', 'првиет'))
