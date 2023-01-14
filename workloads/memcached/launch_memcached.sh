#!/bin/bash
# sudo mkdir /sys/fs/cgroup/memory/memcached

/home/jackson/Documents/linux/tools/perf/perf record -e probe:do_swap_page_L46 -o perf_vdb_$1.data cgexec -g memory:memcached memcached -u jackson -m 30720