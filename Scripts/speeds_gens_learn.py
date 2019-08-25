import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})

avg_speed_evol_no_learn  = [0.00292386, 0.00287577, 0.0035157 , 0.00452804, 0.00569104,
       0.00716522, 0.00831429, 0.00983476, 0.01162949, 0.0133247 ,
       0.01482595, 0.01662248, 0.01797293, 0.019537  , 0.02102718,
       0.02188861, 0.02281816, 0.02396919, 0.02523916, 0.02630479,
       0.02691931, 0.02790836, 0.02885246, 0.02941401, 0.03000109,
       0.03076578, 0.03153322, 0.03237154, 0.03355304, 0.03455728,
       0.03538914, 0.03617292, 0.03687396, 0.03758587, 0.03809967,
       0.03872845, 0.03903253, 0.03940583, 0.03989002, 0.04012019,
       0.04014647, 0.04006294, 0.04032161, 0.04055331, 0.04073364,
       0.04084248, 0.04079565, 0.04074361, 0.04115464, 0.04140497,
       0.0413512 , 0.04165483, 0.0419586 , 0.04249497, 0.04282299,
       0.04317383, 0.0434787 , 0.0436479 , 0.04380292, 0.04363471,
       0.04408234, 0.04483389, 0.04509014, 0.04547065, 0.04548868,
       0.04574277, 0.04606773, 0.04589683, 0.04602418, 0.04622657,
       0.04634821, 0.04619479, 0.04660811, 0.04660938, 0.04654157,
       0.04680223, 0.04727219, 0.04719893, 0.04747164, 0.04744517,
       0.04719592, 0.04735618, 0.04751684, 0.04741797, 0.04735926,
       0.04730233, 0.04718965, 0.0474191 , 0.04743962, 0.04719558,
       0.04704532, 0.04681236, 0.04700715, 0.0473825 , 0.04756558,
       0.0475408 , 0.04776936, 0.04756967, 0.04773088, 0.04756285]


gen_runs = {1:49, 2:34, 3:40, 4:39, 5:31, 6:36, 7:43, 8:35, 9:37, 10:31}

for gens in [30,35,40]:

    avg_runs_l = []
    avg_runs_o = []
    
    best_runs_l = []
    best_runs_o = []
    
    for run in range(1,11):
        if gen_runs[run] < gens:
            continue
        if run == 9:
            continue

        ids_gen = pd.read_csv(f'gids/gen_ids_r{run}.csv')
        
        o_speeds = pd.read_csv(f'o_speed/origin_speed_vals_r{run}_gens_{gens}.csv')
        l_speeds = pd.read_csv(f'l_speed/learned_speed_vals_r{run}_gens_{gens}.csv')
        
        
        ids_in_gen = {}
        for g in range(gens):
            ids = ast.literal_eval(ids_gen[ids_gen['generation']==g]['robot_ids'].values[0])
            ids_in_gen[g] = ids
        
        speed_gen_o = []
        speed_gen_l = []
        
        for g in range(gens):
            ids = ids_in_gen[g]
            learned_gen = l_speeds[l_speeds['id'].isin(ids)]['speed'].values
            origin_gen = o_speeds[o_speeds['id'].isin(ids)]['speed'].values    
            speed_gen_o.append(origin_gen)
            speed_gen_l.append(learned_gen)
            
        learn_avg = [np.nanmean(x) for x in speed_gen_l]
        origin_avg = [np.nanmean(x) for x in speed_gen_o]
        avg_runs_l.append(learn_avg)
        avg_runs_o.append(origin_avg)
        
        learn_best = [np.nanmax(x) for x in speed_gen_l]
        origin_best = [np.nanmax(x) for x in speed_gen_o]    
        best_runs_l.append(learn_best)
        best_runs_o.append(origin_best)    
    
        
    avg_l_all = np.mean(avg_runs_l, axis=0)   
    avg_o_all = np.mean(avg_runs_o, axis=0)   
    avg_best_l_all = np.mean(best_runs_l, axis=0)   
    avg_best_o_all = np.mean(best_runs_o, axis=0)   
        
    l_avg_speed_in_cm = [speed*100 for speed in avg_l_all]
    o_avg_speed_in_cm = [speed*100 for speed in avg_o_all]
    
    l_avg_best_speed_in_cm = [speed*100 for speed in avg_best_l_all]
    o_avg_best_speed_in_cm = [speed*100 for speed in avg_best_o_all]
    l_avg_best_speed_in_cm = [o if o > l else l for o,l in zip(o_avg_best_speed_in_cm, l_avg_best_speed_in_cm)]
    
    no_l_evo_speed_cm = [speed*100 for speed in avg_speed_evol_no_learn]
    no_l_evo_speed_cm = no_l_evo_speed_cm[0:gens]
    
    max_y = (max(l_avg_best_speed_in_cm) if max(l_avg_best_speed_in_cm) > max(l_avg_speed_in_cm) else max(l_avg_speed_in_cm)) * 1.1
    
    learned_speed = [l-o for o,l in zip(o_avg_speed_in_cm, l_avg_speed_in_cm)]
    
    plt.plot(o_avg_speed_in_cm)
    plt.xlabel('Generation')
    plt.ylabel('Learned Speed (cm/s)')
    plt.ylim(0, 2.5)
    
    plt.savefig(f'learned_avg_speed_gen_{gens}.png', bbox_inches='tight')
    plt.clf()    
    
    plt.plot(o_avg_speed_in_cm, color='blue')
    plt.plot(l_avg_speed_in_cm, color='red')
    #plt.plot(no_l_evo_speed_cm, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Speed (cm/s)')
    plt.ylim(0, 15)
    #plt.legend(['origin', 'learned'], loc='lower right')
    #plt.show()
    plt.savefig(f'comp_avg_speed_gen_{gens}.png', bbox_inches='tight')
    plt.clf()
    
    plt.plot(o_avg_best_speed_in_cm, color='blue')
    plt.plot(l_avg_best_speed_in_cm, color='red')
    plt.xlabel('Generation')
    plt.ylabel('Speed (cm/s)')
    plt.ylim(0, 15)
    #plt.legend(['origin', 'learned'], loc='lower right')
    #plt.show()
    plt.savefig(f'comp_avg_best_speed_gen_{gens}.png', bbox_inches='tight')
    plt.clf()

