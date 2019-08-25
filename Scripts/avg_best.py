import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})


runs = 10
generations = 100
pop_size = 100
offspring_size = 50

robots = (generations*offspring_size) + (pop_size-offspring_size)
avg_runs_fitness = []
avg_runs_displacement = []

ms = {}
g_ids = {}
ids_gen_r = {}
for run in range(1, runs+1):
    print(run)
    
    if not os.path.exists(f'results_plane_{run}'):
        os.mkdir(f'results_plane_{run}')
    
    
    measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
    ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')    
    measures['fitness'] = pd.to_numeric(measures['fitness'], errors='coerce')
    measures['displacement_velocity'] = pd.to_numeric(measures['displacement_velocity'], errors='coerce')

    ids_gen = []
    
    for gen in range(0,generations):
        ids_gen.append(ids_snapshots.loc[ids_snapshots['generation'] == gen]['robot_id'].values)
    ids_gen_r[run] = ids_gen
    ms[run] = measures
    g_ids[run] = ids_gen


best_gens_run = []
for run in range(1, runs+1):
    best_per_gen = []
    for gen in range(0,generations):    
        best_per_gen.append(measures[measures['robot_id'].isin(ids_gen_r[run][gen])]['displacement_velocity'].max())
    best_gens_run.append(best_per_gen)
    
    
avg_best_all_runs = np.mean(best_gens_run, axis=0)


plt.plot(avg_best_all_runs*100)
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
plt.savefig(f'results_plane_avg/avg_best_displacement_per_gen.png', bbox_inches='tight')
plt.clf()

