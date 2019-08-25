import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.rcParams.update({'font.size': 16})


gen_runs = {1:49, 2:34, 3:40, 4:39, 5:31, 6:36, 7:43, 8:35, 9:37, 10:31}

for gens in [30, 35, 40]:
    p_desc_runs = []
    for run in range(1,11):
        if gen_runs[run] < gens:
            continue
        if run == 9:
            continue    
        
        ids_gen = pd.read_csv(f'gids/gen_ids_r{run}.csv')  
        p_desc = pd.read_csv(f'pheno/desc_phen_r{run}.csv')
        
        cols = p_desc.columns.values
        
        pdesc_gens = []
        
        for g in range(gens):
            ids = ast.literal_eval(ids_gen[ids_gen['generation']==g]['robot_ids'].values[0])
            avg_gen = p_desc[p_desc['robot_id'].isin(ids)].mean()
            pdesc_gens.append(avg_gen)
        
        p_desc_runs.append(pdesc_gens)
    for col in cols:
        if col == 'robot_id':
            continue
        values = []
        for gen in range(gens):
            gen_vals = []
            for run in range(len(p_desc_runs)):
                gen_vals.append(p_desc_runs[run][gen][col])
            values.append(np.mean(gen_vals))

        col = 'length' if col == 'height' else col
        plt.plot(values, linewidth=3)
        plt.xlabel("Generation")
        ylabel = col.capitalize().replace('_', ' ')
        plt.ylabel(ylabel)
        plt.savefig(f'avg_avg_{col}_gens_{gens}.png', bbox_inches='tight')
        plt.clf()
