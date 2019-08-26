import glob
import pandas as pd

cols = ['robot_id', 'branching', 'branching_modules_count', 'limbs', 'extremities', 'length_of_limbs', 'extensiveness', 'coverage', 'joints', 
'hinge_count', 'active_hinges_count', 'brick_count', 'touch_sensor_count', 'brick_sensor_count', 'proportion', 'width', 'height', 
'absolute_size', 'sensors', 'symmetry', 'avg_period', 'dev_period', 'avg_phase_offset', 'dev_phase_offset', 'avg_amplitude', 
'dev_amplitude', 'avg_intra_dev_params', 'avg_inter_dev_params', 'sensors_reach', 'recurrence', 'synaptic_reception']


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

for exp in range(1, 11):
	folder = experiments[exp]
	df = pd.DataFrame(columns=cols)

	robots = len(glob.glob(f'{folder}phenotype_desc_robot_*'))
	for r_id in range(1,robots+1):
		file = open(f'{folder}phenotype_desc_robot_{r_id}.txt','r')
		row = {}
		row['robot_id'] = r_id
		descriptions = file.read().splitlines()
		for desc in descriptions:
			header, value = desc.split(' ')[0], desc.split(' ')[1]
			row[header]=value
		df = df.append(row, ignore_index=True)

	df.to_csv(f'desc_phen_r{exp}.csv',index=False)
