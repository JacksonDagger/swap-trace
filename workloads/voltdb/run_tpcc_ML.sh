#!/bin/bash
# sudo mkdir /sys/fs/cgroup/memory/voltdb

echo "Starting run with $1M memory"
voltdb_path="./tests/test_apps/tpcc/"

sync; echo 3 > /proc/sys/vm/drop_caches
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled";
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag";
bash -c "echo $1M > /sys/fs/cgroup/memory/voltdb/memory.limit_in_bytes";

cd $voltdb_path
./run.sh clean &&
./run.sh jars &&
/home/jackson/Documents/linux/tools/perf/perf record -e probe:do_swap_page_L46 -o perf_vdb_$1.data cgexec -g memory:voltdb ./run.sh server &
/bin/sleep 10 &&
#./run.sh init &&
../../../bin/sqlcmd < ddl.sql
/bin/sleep 5 &&
start_vdb=$(date +%s%N) && echo "voltdb client started at $start_vdb" &&
./run.sh client | tee xxx.txt
end_vdb=$(date +%s%N)&& echo "voltdb client ended at $end_vdb" && echo "voltdb client run time $((end_vdb-start_vdb)) ns"

sudo kill -9 `pidof java` 