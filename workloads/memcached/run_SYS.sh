# script for running memaslap on memcached

sleep 5

sync; echo 3 > /proc/sys/vm/drop_caches
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled";
bash -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag";
bash -c "echo $1M > /sys/fs/cgroup/memory/memcached/memory.limit_in_bytes";

/home/jackson/Documents/linux/tools/perf/perf record -e probe:do_swap_page_L46 -o perf_mc_SYS_$1.data cgexec -g memory:memcached memcached -u jackson -m 30720 &

sleep 5

memaslap -s 127.0.0.1:11211 -F config_SYS_1.cnf -x 10000000 -S 10s
memaslap -s 127.0.0.1:11211 -F config_SYS_2.cnf -x 10000000 -S 10s

sudo kill -9 `pidof memcached`