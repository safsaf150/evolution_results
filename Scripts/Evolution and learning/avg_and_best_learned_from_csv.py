import numpy as  np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})


speeds = pd.read_csv('speed_vals.csv')
ids_gen = pd.read_csv('ids_in_gen.csv')

avg_speeds = []
best_speeds = []
for gen in range(0,20):
    try:
        ids_in_gen = ids_gen[ids_gen['generation']==gen]['robot_id'].values
        avg_speed_gen = np.mean(speeds[speeds['id'].isin(ids_in_gen)]['speed'])
        best_speed_gen = np.max(speeds[speeds['id'].isin(ids_in_gen)]['speed'])
        avg_speeds.append(avg_speed_gen)
        best_speeds.append(best_speed_gen)
    except:
        pass

avg_speed_in_cm = [speed*100 for speed in avg_speeds]
best_speed_in_cm = [speed*100 for speed in best_speeds]

plt.plot(avg_speed_in_cm)
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
plt.savefig(f'avg_speed_gen.png', bbox_inches='tight')
plt.clf()

plt.plot(best_speed_in_cm)
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
plt.savefig(f'best_speed_gen.png', bbox_inches='tight')
plt.clf()