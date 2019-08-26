import os
import sys
import math
import pandas as pd 
  
gens =  int(sys.argv[1])

data = []

robots = (gens*50) + 50

experiments = {
1:'revolve/experiments/examples/data/learn/1/data_fullevolution/descriptors/',
2:'revolve_r2/experiments/examples/data/learn/2/data_fullevolution/descriptors/',
3:'revolve_r3/experiments/examples/data/learn/3/data_fullevolution/descriptors/',
4:'revolve_r456/experiments/examples/data/learn/4/data_fullevolution/descriptors/',
5:'revolve_r456/experiments/examples/data/learn/5/data_fullevolution/descriptors/',
6:'revolve_r456/experiments/examples/data/learn/6/data_fullevolution/descriptors/',
7:'revolve_r78910/experiments/examples/data/learn/7/data_fullevolution/descriptors/',
8:'revolve_r78910/experiments/examples/data/learn/8/data_fullevolution/descriptors/',
9:'revolve_r78910/experiments/examples/data/learn/9/data_fullevolution/descriptors/',
10:'revolve_r78910/experiments/examples/data/learn/10/data_fullevolution/descriptors/',
}

status = {1:49, 2:34, 3:40, 4:39, 5:31, 6:36, 7:43, 8:35, 9:37, 10:31}


for exp in range(1, 11):
	if status[exp] >= gens:
		folder = experiments[exp]
		for i in range(1, robots+1):
			gen = 1 if i < 101 else math.ceil((i-50)/50)
			file_name = f'{folder}behavior_desc_robot_{i}.txt'
			if os.path.isfile(file_name):
				speed_file = open(file_name, 'r')
				speed = None
				descriptions = speed_file.read().splitlines()
				if len(descriptions) > 1:
					speed = [float(displacement.split(' ')[-1]) for displacement in descriptions if 'displacement_velocity ' in displacement][0]
				data.append([i, speed])

		df = pd.DataFrame(data, columns = ['id', 'speed']) 
		df.to_csv(f'learned_speed_vals_r{exp}_gens_{gens}.csv',index=False)