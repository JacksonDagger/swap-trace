#!/bin/bash
mkdir -p data

for f in $1*.data
do
    out="data/$(basename $f).txt"
    if ! [[ -f "$out" ]]; then
    /home/jackson/Documents/linux/tools/perf/perf script -i $f > $out
    fi
done

chmod -R 777 data