import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import combinations 
plt.rcParams.update({'font.size': 18})

columns = ['branching', 'limbs', 'extremities', 'extensiveness', 'coverage', 'joints', 
         'proportion', 'width', 'length', 'absolute_size', 'symmetry', 'active_hinges_count', 'length_of_limbs']

combos_cols = list(combinations(columns, 2))

amount_first_and_last = 3

for combo in combos_cols:
    try:
        first, second = combo[0], combo[1]
        gen_begin = 0
        gen_end = amount_first_and_last
        gens = np.arange(gen_begin, gen_end)
        x_first = []
        y_first = []
        for run in range(2, 11):
            print(run)
            measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
            measures = measures.rename(columns={'height': 'length'})
            measures.sort_values(by=['robot_id'])
            ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')
            
            robot_ids_gen = ids_snapshots['robot_id'][ids_snapshots['generation'].isin(gens)].values
            robot_ids_gen_u = np.unique(robot_ids_gen)    
            x_first.extend(measures[first][measures['robot_id'].isin(robot_ids_gen_u)].values)
            y_first.extend(measures[second][measures['robot_id'].isin(robot_ids_gen_u)].values)
            
        gen_begin = 100-amount_first_and_last
        gen_end = 100
        gens = np.arange(gen_begin, gen_end)
        x_last = []
        y_last = []
        for run in range(2, 11):
            measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
            measures = measures.rename(columns={'height': 'length'})
            measures.sort_values(by=['robot_id'])
            ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')
            
            robot_ids_gen = ids_snapshots['robot_id'][ids_snapshots['generation'].isin(gens)].values
            robot_ids_gen_u = np.unique(robot_ids_gen)    
            x_last.extend(measures[first][measures['robot_id'].isin(robot_ids_gen_u)].values)
            y_last.extend(measures[second][measures['robot_id'].isin(robot_ids_gen_u)].values)
            
        max_x = max(x_first) if max(x_first) > max(x_last) else max(x_last)        
        max_y = max(y_first) if max(y_first) > max(y_last) else max(y_last)
        max_x = 1 if ((max_x < 1) and (max_x > 0)) else max_x
        max_y = 1 if ((max_y < 1) and (max_y > 0)) else max_y
        x_margin = 0.15*max_x
        y_margin = 0.15*max_y
        max_x += x_margin
        max_y += y_margin            

            
        if not (sum(x_first) == 0 or sum(y_first) == 0 or sum(x_last) == 0 or sum(y_last) == 0):
            sns.set(style="white", color_codes=True, font_scale = 2)
            axis = sns.jointplot(x=x_first, y=y_first, kind='kde', color="skyblue", xlim=(0-x_margin, max_x), ylim=(0-y_margin, max_y), joint_kws={'shade_lowest':False})
            axis.set_axis_labels(first.replace("_", " "), second.replace("_", " "), fontsize=18)
            plt.savefig(f'{first}_{second}_gen_1-3.png', bbox_inches='tight')
            plt.clf()
            
            sns.set(style="white", color_codes=True, font_scale = 2)
            axis = sns.jointplot(x=x_last, y=y_last, kind='kde', color="skyblue", xlim=(0-x_margin, max_x), ylim=(0-y_margin, max_y), joint_kws={'shade_lowest':False})
            axis.set_axis_labels(first.replace("_", " "), second.replace("_", " "), fontsize=18)
            plt.savefig(f'{first}_{second}_gen_98-100.png', bbox_inches='tight')
            plt.clf()

    except:
        plt.clf()
        pass
