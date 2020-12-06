#!/bin/bash
#declare -a benchmarks=("bfs" "pr" "sssp" "cc" "bc" "tc")
declare -a l1_cache_size=(16kB 32kB 64kB)
declare -a l2_cache_size=(128kB 512kB 1MB 2MB)
declare -a l1_cache_associativity=(2 4 8)
declare -a l2_cache_associativity=(2 4 8)
for l1_cache in "${l1_cache_size[@]}"
    do
        for l2_cache in "${l2_cache_size[@]}"
        do 
            for l1_ca in "${l1_cache_associativity[@]}"
            do 
                for l2_ca in "${l2_cache_associativity[@]}"
                do
                    command="./build/X86/gem5.opt -d ~/m5out ./configs/example/se.py -c /home/ics53/gapbs/bfs -o \"-u 9 –n 5\" -I 100000000 --cpu-type=DerivO3CPU --caches --l2cache --l1d_size=${l1_cache} --l1d_assoc=${l1_ca} --l1i_size=${l1_cache} --l1i_assoc=${l1_ca} --l2_size=${l2_cache} --l2_assoc=${l2_ca} --cacheline_size=64 --bp-type=BiModeBP"
                    eval $command
                    mv ~/m5out/stats.txt ~/m5out/stats_${l1_cache}_${l2_cache}_${l1_ca}_${l2_ca}
                 done
            done
       done
   done

#for c_a in "${l1_cache_associativity[@]}"
#    do
#    for benchmark in "${benchmarks[@]}"
#        do 
#            command="./build/X86/gem5.opt -d ~/m5out ./configs/example/se.py -c /home/ics53/gapbs/${benchmark} -o \"-u 9 –n 5\" -I 100000000 --cpu-type=DerivO3CPU --caches --l2cache --l1d_size=16kB --l1d_assoc=${c_a} --l1i_size=16kB --l1i_assoc=${c_a} --l2_size=128kB --l2_assoc=2 --cacheline_size=64 --bp-type=BiModeBP"
#            eval $command
#            mv ~/m5out/stats.txt ~/m5out/stats_${c_a}_${benchmark}.txt
#        done
#    done



