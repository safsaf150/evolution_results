import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})

run = 2
for run in range(1,11):
    print(f'--------------RUN {run}')
    
    measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
    ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')    
    measures['fitness'] = pd.to_numeric(measures['fitness'], errors='coerce')
    measures['displacement_velocity'] = pd.to_numeric(measures['displacement_velocity'], errors='coerce')
    
    ids_in_gen_every_20 = {}
    for i in [1,20,40,60,80,100]:
        ids_in_gen_every_20[i] = ids_snapshots[ids_snapshots['generation']==i-1]['robot_id'].values
    
    
    for i in [1,20,40,60,80,100]:
        best_ten = measures[measures['robot_id'].isin(ids_in_gen_every_20[i])].nlargest(5, ['displacement_velocity']) 
        print(f'--gen {i}--')
        ids = [f'body_robot_{x}.png' for x in best_ten['robot_id'].values]
        print(ids)
    print()