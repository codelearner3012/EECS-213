# GEM-5 Stats Analysis
This project collects GEM5 statistics and analyzes them to calculate and evaluate a cost function. The cost function takes into account the cache hit and miss rates and the clock cycles spent fetching from lower level memory. 

run.sh: bash script to collect and store all the simulation statistics in m5out
cost_function_eval.py: runs through the simulated results and gives out the resulting statistics and optimal configuration based on the calculated cost function.
