# Swap patterns

## Setting up perf probe
### Modifying perf
TODO
### Adding probe
```
sudo ./perf probe --source ../../ --add='do_swap_page:45 vpage=vmf[3] vaddr=vmf[4] entry'
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