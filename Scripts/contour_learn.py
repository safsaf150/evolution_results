import ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import itertools
plt.rcParams.update({'font.size': 18})

columns = ['branching', 'limbs', 'extremities', 'extensiveness', 'coverage', 'joints', 
         'proportion', 'width', 'length', 'absolute_size', 'symmetry', 'active_hinges_count', 'length_of_limbs']

combos_cols = list(itertools.combinations(columns, 2))

amount_first_and_last = 3

gen_runs = {1:49, 2:34, 3:40, 4:39, 5:31, 6:36, 7:43, 8:35, 9:37, 10:31}

#for gens in [30, 35, 40]:

for gens in [40]:
    for combo in combos_cols:
        try:
            first, second = combo[0], combo[1]
            gen_begin = 0
            gen_end = amount_first_and_last
            gens_first = np.arange(gen_begin, gen_end)
            
            gen_begin_last = gens-amount_first_and_last
            gen_end_last = gens
            gens_last = np.arange(gen_begin_last, gen_end_last)
    
            x_first = []
            y_first = []        
            
            x_last = []
            y_last = []
    
            for run in range(1,11):
                if gen_runs[run] < gens:
                    continue
                if run == 9:
                    continue    
                
                ids_gen = pd.read_csv(f'gids/gen_ids_r{run}.csv')  
                
                robot_ids_first = ids_gen[ids_gen['generation'].isin(gens_first)]['robot_ids'].values
                ids_f = [ast.literal_eval(ids) for ids in robot_ids_first]
                ids_f = list(set(list(itertools.chain.from_iterable(ids_f))))
                
                robot_ids_last = ids_gen[ids_gen['generation'].isin(gens_last)]['robot_ids'].values
                ids_l = [ast.literal_eval(ids) for ids in robot_ids_last]
                ids_l = list(set(list(itertools.chain.from_iterable(ids_l))))     
                
                p_desc = pd.read_csv(f'pheno/desc_phen_r{run}.csv')
                p_desc = p_desc.rename(columns={'height': 'length'})
                
                x_first.extend(p_desc[p_desc['robot_id'].isin(ids_f)][first].values)
                y_first.extend(p_desc[p_desc['robot_id'].isin(ids_f)][second].values)
                x_last.extend(p_desc[p_desc['robot_id'].isin(ids_l)][first].values)
                y_last.extend(p_desc[p_desc['robot_id'].isin(ids_l)][second].values)
                
            
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
                plt.savefig(f'{first}_{second}_gen_{gen_begin+1}-{gen_end}.png', bbox_inches='tight')
                plt.clf()
                
                sns.set(style="white", color_codes=True, font_scale = 2)
                axis = sns.jointplot(x=x_last, y=y_last, kind='kde', color="skyblue", xlim=(0-x_margin, max_x), ylim=(0-y_margin, max_y), joint_kws={'shade_lowest':False})
                axis.set_axis_labels(first.replace("_", " "), second.replace("_", " "), fontsize=18)
                plt.savefig(f'{first}_{second}_gen_{gen_begin_last+1}-{gen_end_last}.png', bbox_inches='tight')
                plt.clf()
                
            
        except:
            plt.clf()
            pass
