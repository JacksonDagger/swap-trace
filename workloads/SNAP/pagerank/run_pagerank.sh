# script for running pagerank

sleep 1
sync; echo 3 > /proc/sys/vm/drop_caches
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled";
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag";
bash -c "echo $1M > /sys/fs/cgroup/memory/snap/memory.limit_in_bytes";

/home/jackson/Documents/linux/tools/perf/perf record -e probe:do_swap_page_L46 -o perf_snap_pr_$1.data cgexec -g memory:snap ./pagerank