#!/bin/bash
mkdir data
chmod 666 data

for f in $1*.data
do
    out="data/$f.txt"
    if ! [[ -f "$out" ]]; then
    /home/jackson/Documents/linux/tools/perf/perf script -i $f > $out
    fi
done