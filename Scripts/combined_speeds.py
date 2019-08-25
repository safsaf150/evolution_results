import numpy as  np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})


speeds = pd.read_csv('speed_vals.csv')
origin_speeds = pd.read_csv('origin_speed_vals.csv')
ids_gen = pd.read_csv('ids_in_gen.csv')

avg_speeds = []
best_speeds = []

avg_speeds_origin = []
best_speeds_origin = []

for gen in range(0,20):
    try:
        ids_in_gen = ids_gen[ids_gen['generation']==gen]['robot_id'].values
        avg_speed_gen = np.mean(speeds[speeds['id'].isin(ids_in_gen)]['speed'])
        best_speed_gen = np.max(speeds[speeds['id'].isin(ids_in_gen)]['speed'])
        avg_speeds.append(avg_speed_gen)
        best_speeds.append(best_speed_gen)

        avg_speed_o_gen = np.mean(origin_speeds[origin_speeds['id'].isin(ids_in_gen)]['speed'])
        best_speed_o_gen = np.max(origin_speeds[origin_speeds['id'].isin(ids_in_gen)]['speed'])
        avg_speeds_origin.append(avg_speed_o_gen)
        best_speeds_origin.append(best_speed_o_gen)        
    except:
        pass

avg_speed_in_cm = [speed*100 for speed in avg_speeds]
avg_o_speed_in_cm = [speed*100 for speed in avg_speeds_origin]

best_speed_in_cm = [speed*100 for speed in best_speeds]
best_o_speed_in_cm = [speed*100 for speed in best_speeds_origin]

#for i in range(len(best_speed_in_cm)):
#    best_speed_in_cm[i] = best_speed_in_cm[i] if best_speed_in_cm[i] > best_o_speed_in_cm[i] else best_o_speed_in_cm[i]

plt.plot(avg_o_speed_in_cm, color='blue')
plt.plot(avg_speed_in_cm, color='red')
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
plt.legend(['original speed', 'learned speed'], loc='lower right')
plt.savefig(f'comp_avg_speed_gen.png', bbox_inches='tight')
plt.clf()

plt.plot(best_o_speed_in_cm, color='blue')
plt.plot(best_speed_in_cm, color='red')
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
plt.legend(['original speed', 'learned speed'], loc='lower right')
plt.savefig(f'comp_best_speed_gen.png', bbox_inches='tight')
plt.clf()
