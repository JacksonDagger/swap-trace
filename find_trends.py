import pandas as pd
import numpy as np
from pathlib import Path
from multiprocessing import Pool

def find_trend_leap(deltas, window=None):
    if (window == None):
        window = deltas.size + 1
    maj_index = window - 2
    count = 1

    for i in range(maj_index, -1, -1):
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

    return (count >= (window/2)), candidate

def find_stride(deltas, window):
    stride = deltas[0]
    if np.all(deltas[:window - 1] == stride):
        return True, stride
    return False, 0

def find_trends_optimized(deltas, windows=(2,)):
    arrlens = []
    leap_results = []
    stride_results = []
    stride_lengths = []

    for window in windows:
        arrlens.append(deltas.shape[0] - window + 1)
        leap_results.append(np.empty((arrlens[-1]), dtype=np.bool8))
        stride_results.append(np.empty((arrlens[-1]), dtype=np.bool8))
        stride_lengths.append(np.empty((arrlens[-1]), dtype=np.uint64))

    for i in range(max(arrlens)):
        if i >= min(arrlens):
            for j, window in enumerate(windows):
                if i < arrlens[j]:
                    leap_results[j][i] = find_trend_leap(deltas[i:], window=window)[0]
                    stride = find_stride(deltas[i:], window=window)
                    stride_results[j][i] = stride[0]
                    stride_lengths[j][i] = stride[1]
        else:
            for j, window in enumerate(windows):
                leap_results[j][i] = find_trend_leap(deltas[i:], window=window)[0]
                stride = find_stride(deltas[i:], window=window)
                stride_results[j][i] = stride[0]
                stride_lengths[j][i] = stride[1]

    return leap_results, stride_results, stride_lengths

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
    print(str(filename) + " starting.")
    df = pd.read_csv(filename, index_col=0)
    # df = df[df["page"] == 0]
    df["time"] = df["time"].to_numpy()
    arr = df[df.columns.difference(["time"], sort=False)].to_numpy(dtype=np.uint64)
    deltas = np.diff(arr, axis=0)
    #print(deltas.dtype)
    #np.savetxt("deltas.csv", deltas, delimiter=",", fmt='%lu')
    #print(df.head())
    #print(deltas)
    windows = (2, 3, 4, 8, 16, 32)
    v_leap_trends, v_stride_trends, v_stride_lengths = find_trends_optimized(deltas[:,0], windows=windows)
    p_leap_trends, p_stride_trends, p_stride_lengths = find_trends_optimized(deltas[:,2], windows=windows)
    ret = {
        "file": str(filename)
    }
    
    ret["mB"] = str(filename).split(".")[0].split("_")[-1]
    for window, vt, pt in zip(windows, v_leap_trends, p_leap_trends):
        v0p0 = np.count_nonzero(np.logical_and(np.logical_not(vt), np.logical_not(pt)))
        v0p1 = np.count_nonzero(np.logical_and(np.logical_not(vt), pt))
        v1p0 = np.count_nonzero(np.logical_and(vt, np.logical_not(pt)))
        v1p1 = np.count_nonzero(np.logical_and(vt, pt))
        ret["w" + str(window) + "_v0p0_leap"] = v0p0
        ret["w" + str(window) + "_v0p1_leap"] = v0p1
        ret["w" + str(window) + "_v1p0_leap"] = v1p0
        ret["w" + str(window) + "_v1p1_leap"] = v1p1

        ret["w" + str(window) + "_n_leap"] = v0p0 + v0p1 + v1p0 + v1p1
        ret["w" + str(window) + "_phi_leap"] = phi_coefficient(v1p1, v0p0, v1p0, v0p1)

    for window, vt, pt in zip(windows, v_stride_trends, p_stride_trends):
        v0p0 = np.count_nonzero(np.logical_and(np.logical_not(vt), np.logical_not(pt)))
        v0p1 = np.count_nonzero(np.logical_and(np.logical_not(vt), pt))
        v1p0 = np.count_nonzero(np.logical_and(vt, np.logical_not(pt)))
        v1p1 = np.count_nonzero(np.logical_and(vt, pt))
        ret["w" + str(window) + "_v0p0_stride"] = v0p0
        ret["w" + str(window) + "_v0p1_stride"] = v0p1
        ret["w" + str(window) + "_v1p0_stride"] = v1p0
        ret["w" + str(window) + "_v1p1_stride"] = v1p1

        ret["w" + str(window) + "_n_stride"] = v0p0 + v0p1 + v1p0 + v1p1
        ret["w" + str(window) + "_phi_stride"] = phi_coefficient(v1p1, v0p0, v1p0, v0p1)

    for window, v_len, p_len in zip(windows, v_stride_lengths, p_stride_lengths):
        v_nopattern = np.count_nonzero(v_len == 0)
        v_step = np.count_nonzero(v_len == 4096)
        v_stride = np.count_nonzero(v_len < 0) +  np.count_nonzero(v_len > 4096)
        v_n = v_nopattern + v_step + v_stride

        p_nopattern = np.count_nonzero(p_len == 0)
        p_step = np.count_nonzero(p_len == 1)
        p_stride = np.count_nonzero(p_len < 0) +  np.count_nonzero(p_len > 1)
        p_n = p_nopattern + p_step + p_stride

        ret["w" + str(window) + "_v_nopattern"] = v_nopattern
        ret["w" + str(window) + "_v_step"] = v_step
        ret["w" + str(window) + "_v_stride"] = v_stride
        ret["w" + str(window) + "_v_n"] = v_n

        ret["w" + str(window) + "_p_nopattern"] = p_nopattern
        ret["w" + str(window) + "_p_step"] = p_step
        ret["w" + str(window) + "_p_stride"] = p_stride
        ret["w" + str(window) + "_p_n"] = p_n

    #dflist.append(ret)
    print(str(filename) + " finished.")
    return ret

files = Path("traces").glob('*')
"""
for f in list(files)[:1]:
    dflist = []
    dflist.append(parse_output(f))
    df = pd.DataFrame(dflist)
    df.to_csv("results-test.csv")
"""
with Pool(processes=16) as pool:
    dflist = pool.map(parse_output, files)
    df = pd.DataFrame(dflist)
    df.to_csv("results.csv")

