import os
import numpy as np
def area_calculation(l1_cs, l2_cs, l1_a, l2_a):
    l1_cc = {"16kB":100, "32kB":200, "64kB":400}
    l2_cc = {"128kB":25 , "512kB":75 ,"1MB":100, "2MB":200}
    cost = l1_cc[l1_cs] + l2_cc[l2_cs] + l1_a + l2_a
    return int(cost)


access_latency = {"16kB":3, "32kB":3, "64kB":3, "128kB":9, "512kB": 18, "1MB":24, "2MB":33}
base = 1000000000000
variables_to_read = ["sim_seconds", "system.cpu.cpi_total", "system.cpu.dcache.overall_miss_rate::total", "system.cpu.dcache.overall_avg_miss_latency::total","system.cpu.icache.overall_miss_rate::total", "system.cpu.icache.overall_avg_miss_latency::total", "system.l2.overall_miss_rate::total", "system.l2.overall_avg_miss_latency::total"]

v_v_2 = ["sim_seconds", "system.cpu.dcache.overall_hits::total", "system.cpu.dcache.overall_miss_latency::total", "system.cpu.icache.overall_hits::total", "system.cpu.icache.overall_miss_latency::total"] 

#["system.l2.overall_hits::total", "system.l2.overall_miss_latency::total"]

config = []
measurement_list = []
minValue = 0.0
minConfig = ""
files = filter(os.path.isfile, os.listdir( os.curdir ))
for file in files:
    if file.startswith("stats"):
        filename = file.split("_")
        l1_cs = filename[1]
        l2_cs = filename[2]
        l1_a = int(filename[3])
        l2_a = int(filename[4])
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
                elif x[0] in v_v_2: 
                    y = x[1].strip()
                    y = y.split("#")[0]
                    #print y
                    total_latency = total_latency + int(y)
            total_latency = total_latency + dcache_hit_lat + icache_hit_lat
            cache_time = round(float(total_latency)/base, 6)
            area_cost = area_calculation(l1_cs, l2_cs, l1_a, l2_a)
            total_calc_cost = round(area_cost * cache_time, 6)
            total_eval_cost = round(area_cost * sim_seconds, 6)
            config.append(file)
            # 1. cache_time: latency measurement 
            # 2. area_cost : self defined cost of the area of a cache 
            # 3. total = producet of the cache_time and area_cost
            measurement_list.append([sim_seconds, cache_time, area_cost, total_calc_cost, total_eval_cost])

Y = np.array(measurement_list)

#minimum sim_seconds config 
min_ss_seconds = np.min(Y[:,0])
print "Configurations with the minimum sim_seconds = " + str(min_ss_seconds)
for i,c in enumerate(config):
    if Y[i][0] == min_ss_seconds:
        print c

#minimum latency
min_latency= np.min(Y[:,1])
print "Configurations with the minimum latency = " + str(min_latency)
for i,c in enumerate(config):
    if Y[i][1] == min_latency:
        print c


#minimum area-cost
min_area_cost = np.min(Y[:,2])
print "Configurations with the minimum area_cost = " + str(min_area_cost)
for i,c in enumerate(config):
    if Y[i][2] == min_area_cost:
        print c


#minimum total cost 
min_total_cost = np.min(Y[:, 3])
print "Configurations with the minimum total_cost = " + str(min_total_cost)
for i,c in enumerate(config):
    if Y[i][3] == min_total_cost:
        print c



for i,c in enumerate(config):
    print c + " " + str(measurement_list[i])

#evaluation takes in sim_seconds
#min_eval_cost = np.min(Y[:,4])

#elif x[0]=="system.l2.overall_hits::total":
#                    y = x[1].strip()
#                    y = y.split("#")[0]
#                    l2_cache_hits = y
#                    l2_cache_hit_lat = int(y) * access_latency[l2_cs]
#                    print l2_cache_hits + " * " + str(access_latency[l2_cs])

