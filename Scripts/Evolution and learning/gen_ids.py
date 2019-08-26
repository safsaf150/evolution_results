import glob
import pandas as pd

experiments = {
1:'revolve/experiments/examples/data/learn/1/',
2:'revolve_r2/experiments/examples/data/learn/2/',
3:'revolve_r3/experiments/examples/data/learn/3/',
4:'revolve_r456/experiments/examples/data/learn/4/',
5:'revolve_r456/experiments/examples/data/learn/5/',
6:'revolve_r456/experiments/examples/data/learn/6/',
7:'revolve_r78910/experiments/examples/data/learn/7/',
8:'revolve_r78910/experiments/examples/data/learn/8/',
9:'revolve_r78910/experiments/examples/data/learn/9/',
10:'revolve_r78910/experiments/examples/data/learn/10/',
}


for i in range(1, 11):
	folder = experiments[i]
	s_folders = glob.glob(f'{folder}selectedpop*')

	generation_ids = {}

	for gen in range(0, len(s_folders)):
		robots = glob.glob(f'{folder}selectedpop_{gen}/body_robot*')
		ids = [int(id.split('.')[0].split('_')[-1]) for id in robots]
		generation_ids[gen] = ids
		
	df = pd.DataFrame(list(generation_ids.items()), columns=['generation', 'robot_ids'])

	df.to_csv(f'gen_ids_r{i}.csv',index=False)