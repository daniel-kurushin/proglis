from matplotlib import pyplot as plt
from utilites import load, dump, compare

_in = load('test2.json')

russia = _in['Российская Федерация']
tatars = _in['Республика Татарстан']

with open('Российская Федерация.dot','w') as dot:
    dot.write("digraph g {\n")
    dot.write('\t" " [shape = none];\n\toverlap = false;\n\tsep=-0.8\n')
    for mat, val in russia.items():
        if mat != "avg":
            dot.write('\t"%s" [shape = none, fontsize = %s, fontname="sans"]\n' % (mat.replace(' ','\\n'), val * 30))
    for mat, val in russia.items():
        if mat != "avg":
            dot.write('\t" " -> "%s" [style=invis] \n' % mat.replace(' ','\\n'))
    dot.write("}\n")
        
with open('Республика Татарстан.dot','w') as dot:
    dot.write("digraph g {\n")
    dot.write('\t" " [shape = none];\n\toverlap = false;\n\tsep=-0.8\n')
    for mat, val in tatars.items():
        if mat != "avg":
            fontsize = 30 * val ** 2 if val > 0 else 10
            dot.write('\t"%s" [shape = none, fontsize = %s, fontname="sans"]\n' % (mat.replace(' ','\\n'), fontsize))
    for mat, val in russia.items():
        if mat != "avg":
            dot.write('\t" " -> "%s" [style=invis] \n' % mat.replace(' ','\\n'))
    dot.write("}\n")
        
    