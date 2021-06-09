import sys
import os
import re

folder = sys.argv[1]

filenames = os.listdir(folder)
filenames = [x for x in filenames if "0." in x]

re_exp = re.compile("[0-9\.]+%")

def repl(x):
    return "({}*0.01)".format(x[0][:-1])

for filename in filenames:
    try:
        with open(os.path.join(folder, filename)) as fin:
            cnt = 0
            acc = 0
            for line in fin:
                exp1 = line.strip().split(" ")[0]
                exp2 = " ".join(line.strip().split(" ")[1:])
                exp1 = re_exp.sub(repl, exp1)
                exp2 = re_exp.sub(repl, exp2)
                cnt += 1
                try:
                    if eval(exp1) == eval(exp2):
                        acc += 1
                except:
                    pass
            print(filename, acc/cnt)
    except:
        continue
