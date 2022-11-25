import pandas as pd
from pathlib import Path

def read_perf_output(filename, event=None):
    with open(filename) as file:
        lines = file.readlines()
        dflist = []
        if (event == None):
            for line in lines:
                words = line.split()
                i = 3
                while ("." not in words[i]):
                    i += 1
                d = {
                    "time" : float(words[i][:-1])
                }

                for word in words[i+3:]:
                    parts = word.split("=")
                    d[parts[0]] = int(parts[1], base=16)
                dflist.append(d)
        else:
            for line in lines:
                if event in line:
                    words = line.split()
                    i = 3
                    while ("." not in words[i]):
                        i += 1
                    d = {
                        "time" : float(words[i][:-1])
                    }

                    for word in words[6:]:
                        parts = word.split("=")
                        d[parts[0]] = int(parts[1], base=16)
                    dflist.append(d)
        
        return pd.DataFrame(dflist)

outpath = Path("traces/")
outpath.mkdir(parents=True, exist_ok=True)
files = Path("data").glob('*')

for f in files:
    print(f)
    df = read_perf_output(f)
    outfile = f.stem + ".csv"
    df.to_csv(outpath/outfile)