"""
Returns number of sequences and aminoacids in all given fasta files and aminoacids' occurrence in html table (stdout)

python protstat.py [fasta files]
"""
from sys import argv
from collections import Counter
import pandas as pd

pd.set_option('display.float_format', lambda x: '%.3f' % x)


def read_fasta(fl):
    """reads one fasta file, returns [<number of sequences>, Counter<aa>]"""
    res = [0, Counter()]
    with open(fl, 'r') as fin:
        for raw_line in fin:
            line = raw_line.strip()
            if line[0] == '>':
                res[0] += 1
                continue
            res[1] += Counter(line)
    return res


x = []
for fle in argv[1:]:
    x.append(read_fasta(fle))
df = pd.DataFrame.from_dict(x[0][1], orient='index').transpose()*100/sum(x[0][1].values())
print(x[0][0])
for el in x[1:]:
    print(el[0])
    df = df.append(pd.DataFrame.from_dict(el[1], orient='index').transpose()*100/sum(el[1].values()))
colnum = len(df)
df = df.transpose()
df.columns = [x for x in range(colnum)]
df['diff 1-2'] = df[0] - df[1]
print(df.to_html())
