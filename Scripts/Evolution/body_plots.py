import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})


runs = 10
generations = 100
pop_size = 100
offspring_size = 50
robots = (generations*offspring_size) + (pop_size-offspring_size)
measures = pd.read_csv(f'1/all_measures.tsv', sep='\t')
gen_data = {}

columns = measures.columns


ms = []
ids = []

for run in range(2,11):
    measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
    
    # coerce errors
    measures['fitness'] = pd.to_numeric(measures['fitness'], errors='coerce')
    measures['displacement_velocity'] = pd.to_numeric(measures['displacement_velocity'], errors='coerce')
    measures['head_balance'] = pd.to_numeric(measures['head_balance'], errors='coerce')
    measures['contacts'] = pd.to_numeric(measures['contacts'], errors='coerce')
    measures['displacement_velocity_hill'] = pd.to_numeric(measures['displacement_velocity_hill'], errors='coerce')    
    measures['run'] = run
    ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')
    ids_snapshots['run'] = run
    ms.append(measures)
    ids.append(ids_snapshots)
        
all_measures = pd.concat(ms)
all_ids_snapshots = pd.concat(ids)

data_per_gen = []

for gen in range(0, 100):
    gen_dfs = []
    for run in range(2,11):
        ids_of_gen = all_ids_snapshots[(all_ids_snapshots['run'] == run) & (all_ids_snapshots['generation'] == gen)]['robot_id'].values
        gen_ms_r = all_measures[(all_measures['run'] == run) & (all_measures['robot_id'].isin(ids_of_gen))]
        gen_dfs.append(gen_ms_r)
    data_per_gen.append(pd.concat(gen_dfs))


for column in columns:
    if column not in ['robot_id', 'run']:
        try:
            
            avg_runs_gens = [np.mean(x[column].values)*100 for x in data_per_gen] if 'displacement' in column else [np.mean(x[column].values) for x in data_per_gen]
            min_runs_gens = [np.min(x[column].values)*100 for x in data_per_gen] if 'displacement' in column else [np.min(x[column].values) for x in data_per_gen]
            max_runs_gens = [np.max(x[column].values)*100 for x in data_per_gen] if 'displacement' in column else [np.max(x[column].values) for x in data_per_gen]

##          avg of min and max of runs
#            min_runs_gens = []
#            max_runs_gens = []
#                
#            for x in data_per_gen:
#                min_vals_gen = []
#                max_vals_gen = []
#                for run in range(2,11):
#                    min_vals_gen.append(np.min(x[x['run']==run][column].values))
#                    max_vals_gen.append(np.max(x[x['run']==run][column].values))
#                mean_min = np.mean(min_vals_gen) * 100 if 'displacement' in column else np.mean(min_vals_gen)
#                mean_max = np.mean(max_vals_gen) * 100 if 'displacement' in column else np.mean(max_vals_gen)
#                min_runs_gens.append(mean_min)
#                max_runs_gens.append(mean_max)                  
            
            x=np.arange(0,100)
            plt.plot(x, avg_runs_gens, linewidth=3)
            plt.fill_between(x, y1=min_runs_gens, y2=max_runs_gens, alpha=0.5)
            plt.xlabel("Generation")
            ylabel = column.capitalize().replace('_', ' ')
            ylabel = 'Speed (cm/s)' if column == 'displacement_velocity' else ylabel
            plt.ylabel(ylabel)
            plt.savefig(f'min_max_avg_{column}.png', bbox_inches='tight')
            #plt.savefig(f'avg_{column}.png', bbox_inches='tight')
            plt.clf()
        except Exception as e:
            print(f'ERROR, failed to draw plot for {column}')
            print(e)
            pass

