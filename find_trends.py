import pandas as pd
import numpy as np
from pathlib import Path

def find_trend_leap(deltas, window=None):
    if (window == None):
        window = deltas.size
    maj_index = window - 1
    count = 1

    for i in range(maj_index - 1, -1):
        if (deltas[i] == deltas[maj_index]):
            count += 1
        else:
            count -= 1
        
        if (count == 0):
            maj_index = i
            count = 1
    candidate = deltas[maj_index]

    count = 0
    for i in range(0, window-1):
        if (deltas[i] == candidate):
            count += 1

    return (count > (window/2)), candidate

def find_trends(deltas, windows=(2,)):
    results = []
    for window in windows:
        arrlen = deltas.shape[0] - window + 1
        result = np.empty((arrlen), dtype=np.bool8)
        for i in range(arrlen):
            result[i] = find_trend_leap(deltas[i:], window=window)[0]
        results.append(result)
    return results

def phi_coefficient(n11, n00, n10, n01):
    denom_sq = (n11+n10)*(n11+n01)*(n00+n10)*(n00+n01)
    if denom_sq == 0:
        return 0
    return (n11*n00 - n10*n01)/np.sqrt(float(denom_sq))


def parse_output(filename):
    df = pd.read_csv(filename)
    times = df["time"].to_numpy()
    arr = df[df.columns.difference(["time"])].to_numpy()
    deltas = np.diff(arr, axis=0)

    windows = (2, 4, 8, 16, 32)
    v_trends = find_trends(deltas[:,0], windows=windows)
    p_trends = find_trends(deltas[:,2], windows=windows)
    ret = {
        "file": str(filename)
    }
    
    ret["mB"] = str(filename).split(".")[0].split("_")[-1]
    for window, vt, pt in zip(windows, v_trends, p_trends):
        v0p0 = np.count_nonzero(np.logical_and(np.logical_not(vt), np.logical_not(pt)))
        v0p1 = np.count_nonzero(np.logical_and(np.logical_not(vt), pt))
        v1p0 = np.count_nonzero(np.logical_and(vt, np.logical_not(pt)))
        v1p1 = np.count_nonzero(np.logical_and(vt, pt))
        ret["w" + str(window) + "_v0p0"] = v0p0
        ret["w" + str(window) + "_v0p1"] = v0p1
        ret["w" + str(window) + "_v1p0"] = v1p0
        ret["w" + str(window) + "_v1p1"] = v1p1

        ret["w" + str(window) + "_n"] = v0p0 + v0p1 + v1p0 + v1p1
        ret["w" + str(window) + "_phi"] = phi_coefficient(v1p1, v0p0, v1p0, v0p1)

    return ret

files = Path("traces").glob('*')
dflist = []

for f in files:
    print(f)
    dflist.append(parse_output(f))

df = pd.DataFrame(dflist)
df.to_csv("results.csv")