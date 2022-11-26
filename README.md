# Swap patterns

## Setting up perf probe
### Modifying perf
Clone linux from https://github.com/JacksonDagger/linux.git and change branches the v5.19-perf-pointer branch. Build and install linux as usual and then build the modified perf with the following commands.
```
cd tools/perf
make
```
The perf binary can then be found in tools/perf. Alternatively, you can apply 0001-perf-force-size.patch to another version of linux. However, it's only tested on 5.19.
### Adding probe
The probe can then be added to perf with the following command.
```
sudo ./perf probe --source ~/Documents/linux --force-size=8 --add='do_swap_page:46 vpage=vmf[3] vaddr=vmf[4] vmf->orig_pte.pte page'
```
## Creating traces
With the probe created, run any program, restricted to `$M` megabytes of memory with the following commands. A cgroup must also be created first. These commands require the script to be run as superuser.
```
bash -c "echo $M M > /sys/fs/cgroup/$GROUP/memory.high";
[linux location]/linux/tools/perf/perf record -e probe:do_swap_page_L46 -o perf_$PROGNAME_$M.data cgexec -g memory:$GROUP $COMMAND
```
The file perf_$PROGNAME_$M.data can then be output to text using the export.sh script, modified for the perf data file locations. Running make_traces.py will then convert the text output into csv traces for analyzing.

## Analyzing traces
### Pattern analysis
Running find_trends.py will apply LEAP's trend detection tool on both page offsets and virtual page addresses.

### Simulated prefetcher
TODO
### Visualization
TODO