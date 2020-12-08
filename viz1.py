from matplotlib import pyplot as plt
from utilites import load, dump, compare

_in = load('test1.json')
регионы = load('регионы.json')
rf = load('rf.json')

for k in rf.keys():
    _in[k].update({'Российская Федерация':rf[k]})
    
data = {}
for reg_a in регионы:
    row = {}
    for mat in _in.keys():
        found = 0
        for reg_b, idx in _in[mat].items():
            if compare(reg_a.lower(), reg_b.lower()) > 0.9:
                row.update({mat.capitalize():1 - idx})
                found = 1
        if not found:
            row.update({mat.capitalize():0})

    data.update({reg_a:row})

for reg in data.keys():
    x = 0
    n = 0
    for mat in data[reg].keys():
        x += data[reg][mat]
        n += 1
    x = x / n
    data[reg].update({'avg':x})
dump(data, 'test2.json')

with open('out.csv','w') as csv:
    csv.write('\t')
    for mat in data["Российская Федерация"].keys():
        csv.write('"%s"\t' % mat)
    csv.write('\n')

    for reg in data.keys():
        csv.write('"%s"\t' % reg)
        for mat in data[reg].keys():
            csv.write('%s\t' % str(data[reg][mat]).replace('.', ','))
        csv.write('\n')

#with open("%s.csv" % mat, "w") as f:
#    for idx, reg in sorted(data):
#        f.write('"%s"\t%s\n' % (reg, str(round(idx,4)).replace('.',',')))

        
