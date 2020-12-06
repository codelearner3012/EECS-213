import os

#def cost_function_calculation(l1_cs, l2_cs, l1_a, l2_a, cache_latency):
#    stw = {"16kB":16, "32kB":32, "64kB":64, "128kB":128, "512kB": 512, "1MB":1024, "2MB":2048}
#    cost = stw[l1_cs]*l1_a + stw[l2_cs]*l2_a
#    return cost


access_latency = {"16kB":3, "32kB":3, "64kB":3, "128kB":9, "512kB": 18, "1MB":24, "2MB":33}
base = 1000000000000
variables_to_read = ["sim_seconds", "system.cpu.cpi_total", "system.cpu.dcache.overall_miss_rate::total", "system.cpu.dcache.overall_avg_miss_latency::total","system.cpu.icache.overall_miss_rate::total", "system.cpu.icache.overall_avg_miss_latency::total", "system.l2.overall_miss_rate::total", "system.l2.overall_avg_miss_latency::total"]

v_v_2 = ["sim_seconds", "system.cpu.dcache.overall_hits::total", "system.cpu.dcache.overall_miss_latency::total", "system.cpu.icache.overall_hits::total", "system.cpu.icache.overall_miss_latency::total", "system.l2.overall_hits::total", "system.l2.overall_miss_latency::total"]

files = filter(os.path.isfile, os.listdir( os.curdir ))
for file in files:
    if file.startswith("stats"):
        filename = file.split("_")
        l1_cs = filename[1]
        l2_cs = filename[2]
        l1_a = filename[3]
        l2_a = filename[4]
        total_latency = 0
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                x = line.split(" ", 1)
                if x[0]=="sim_seconds":
                    y = x[1].strip()
                    y = y.split("#")[0]
                    sim_seconds = float(y)
                elif x[0]=="system.cpu.dcache.overall_hits::total":
                    y = x[1].strip()
                    y = y.split("#")[0]
                    dcache_num_hits = y
                    dcache_hit_lat = int(y)* access_latency[l1_cs]
                    #print dcache_num_hits + " * " + str(access_latency[l1_cs])
                elif x[0]=="system.cpu.icache.overall_hits::total":
                    y = x[1].strip()
                    y = y.split("#")[0]
                    icache_num_hits = y
                    icache_hit_lat = int(y) * access_latency[l1_cs]
                    #print icache_num_hits + " * " + str(access_latency[l1_cs])
                elif x[0]=="system.l2.overall_hits::total":
                    y = x[1].strip()
                    y = y.split("#")[0]
                    l2_cache_hits = y
                    l2_cache_hit_lat = int(y) * access_latency[l2_cs]
                    #print l2_cache_hits + " * " + str(access_latency[l2_cs])
                elif x[0] in v_v_2: 
                    y = x[1].strip()
                    y = y.split("#")[0]
                    #print y
                    total_latency = total_latency + int(y)
            total_latency = total_latency + dcache_hit_lat + icache_hit_lat + l2_cache_hit_lat
            cache_time = round(float(total_latency)/base, 6)
            print file + "---> sim_seconds " + str(sim_seconds) + " " + str(cache_time)
            #print str(sim_seconds-cache_time)
            #attempt at calculating the cost function

                   

