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
sudo ./perf probe --source ~/Documents/linux --force-size=8 --add='do_swap_page:45 vpage=vmf[3] vaddr=vmf[4] vmf->orig_pte.pte'
```
## Creating traces
TODO

## Analyzing traces
### Pattern analysis
TODO
### Simulated prefetcher
TODO
### Visualization
TODO