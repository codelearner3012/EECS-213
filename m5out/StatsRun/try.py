import os

access_latency = {8:3, 32:3, 64:3, 128:9, 512: 18, 1:24, 2:33}

variables_to_read = ["sim_seconds", "system.cpu.cpi_total", "system.cpu.dcache.overall_miss_rate::total", "system.cpu.dcache.overall_avg_miss_latency::total","system.cpu.icache.overall_miss_rate::total", "system.cpu.icache.overall_avg_miss_latency::total", "system.l2.overall_miss_rate::total", "system.l2.overall_avg_miss_latency::total"]

v_v_2 = ["sim_seconds", "system.cpu.dcache.overall_hits::total", "system.cpu.dcache.overall_miss_latency::total", "system.cpu.icache.overall_hits::total", "system.cpu.icache.overall_miss_latency::total", "system.l2.overall_hits::total", "system.l2.overall_miss_latency::total"]

files = filter(os.path.isfile, os.listdir( os.curdir ))
for file in files:
    print file
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            x = line.split(" ", 1)
            if x[0] in v_v_2:
                s = x[1].strip()
                print x[0] + "->" + s.split("#")[0]
            

