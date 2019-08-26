import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

run = 1

generations = 5
pop_size = 5
offspring_size = 2

if not os.path.exists(f'learning_{run}'):
    os.mkdir(f'learning_{run}')
if not os.path.exists(f'learning_{run}/stats'):
    os.mkdir(f'learning_{run}/stats')

robots = (generations*offspring_size) + (pop_size-offspring_size)

measures = pd.read_csv(f'plane_learning_{run}/all_measures.tsv', sep='\t')
ids_snapshots = pd.read_csv(f'plane_learning_{run}/snapshots_ids.tsv', sep='\t')

ids_gen = []

for gen in range(0,generations):
    ids_gen.append(ids_snapshots.loc[ids_snapshots['generation'] == gen]['robot_id'].values)
    

d_velocity_vals = []
for gen_ids in ids_gen:
    velocity_gen = []
    for r_id in gen_ids:
        velocity_gen.append(float(measures.loc[measures['robot_id'] == r_id]['displacement_velocity'].values[0]))
    d_velocity_vals.append(velocity_gen)

d_avg_vel_vals_per_gen = [np.mean(vel_list) for vel_list in d_velocity_vals]


d_vel_vals_all_robots = []
for r_id in range(1, robots+1):
    d_vel_vals_all_robots.append(measures.loc[measures['robot_id'] == r_id]['displacement_velocity'].astype(float).values[0])

fitness_vals = []
for gen_ids in ids_gen:
    fitness_gen = []
    for r_id in gen_ids:
        fitness_gen.append(float(measures.loc[measures['robot_id'] == r_id]['fitness'].values[0]))
    fitness_vals.append(fitness_gen)

avg_fitness_vals_per_gen = [np.mean(fitness_list) for fitness_list in fitness_vals]


fitness_vals_all_robots = []
for r_id in range(1, robots+1):
    fitness_vals_all_robots.append(measures.loc[measures['robot_id'] == r_id]['fitness'].astype(float).values[0])


# avg displacement velocity per generation
plt.plot(np.arange(1, generations+1, 1), d_avg_vel_vals_per_gen)
plt.xticks(range(1, generations+1))
plt.ylabel('displacement velocity')
plt.title('avg displacement velocity per generation')
plt.savefig(f'learning_{run}/stats/avg_displace_vel_per_gen.png')
plt.clf()

# displacement velocity per robot
plt.plot(np.arange(1, robots+1), d_vel_vals_all_robots)
plt.ylabel('displacement velocity')
plt.title('displacement velocity per robot')
plt.savefig(f'learning_{run}/stats/displ_vel_per_robot.png')
plt.clf()

# avg fitness per generation
plt.plot(np.arange(1, generations+1, 1), avg_fitness_vals_per_gen)
plt.xticks(range(1, generations+1))
plt.ylabel('fitness')
plt.title('avg fitness per generation')
plt.savefig(f'learning_{run}/stats/avg_fitness_gen.png')
plt.clf()

# fitness per robot
plt.plot(np.arange(1, robots+1), fitness_vals_all_robots)
plt.ylabel('fitness')
plt.title('fitness per robot')
plt.savefig(f'learning_{run}/stats/fitness_robots.png')
plt.clf()

# correlation heat map
plt.figure(figsize=(30,30))
sns.heatmap(measures.corr(),
            vmin=-1,
            cmap='coolwarm',
            annot=True);
plt.savefig(f'learning_{run}/stats/corr_matrix.png')
plt.clf()

