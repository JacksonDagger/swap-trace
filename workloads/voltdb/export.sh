#!/bin/bash
for f in *.data
do
    out="$f.txt"
    if ! [[ -f "$out" ]]; then
    /home/jackson/Documents/linux/tools/perf/perf script -i $f > $out
    fi
done