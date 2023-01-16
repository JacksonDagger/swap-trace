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
                        if parts[0] == "pte":
                            d[parts[0]] = int("0x" + parts[1][-8:], base=16)
                        else:
                            d[parts[0]] = int(parts[1], base=16)
                    dflist.append(d)
        
        return pd.DataFrame(dflist)

outpath = Path("traces/")
outpath.mkdir(parents=True, exist_ok=True)
files = Path("results").glob('*')

skipfiles = ["results/perf_mc_ETC_1244.data.txt",
            "results/perf_mc_ETC_829.data.txt",
            "results/perf_mc_ETC_415.data.txt",
            "results/perf_mc_SYS_2150.data.txt",
            "results/perf_mc_SYS_1434.data.txt",
            "results/perf_mc_SYS_717.data.txt",
            "results/perf_snap_pr_77.data.txt",
            "results/perf_snap_pr_51.data.txt",
            "results/perf_snap_pr_26.data.txt",
            ]

for f in files:
    if str(f) in skipfiles:
        continue
    print(f)
    df = read_perf_output(f)
    outfile = f.stem + ".csv"
    df.to_csv(outpath/outfile)