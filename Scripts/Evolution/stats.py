import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

run = 5
generations = 100
pop_size = 100
offspring_size = 50

robots = (generations*offspring_size) + (pop_size-offspring_size)


if not os.path.exists(f'results_plane_{run}'):
    os.mkdir(f'results_plane_{run}')

measures = pd.read_csv(f'{run}/all_measures.tsv', sep='\t')
ids_snapshots = pd.read_csv(f'{run}/snapshots_ids.tsv', sep='\t')

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
plt.plot(d_avg_vel_vals_per_gen)
plt.ylabel('displacement velocity')
plt.title('avg displacement velocity per generation')
plt.savefig(f'results_plane_{run}/avg_displacement_per_gen.png')
plt.clf()

# displacement velocity per robot
plt.plot(d_vel_vals_all_robots)
plt.ylabel('displacement velocity')
plt.title('displacement velocity per robot')
plt.savefig(f'results_plane_{run}/displacement_per_robot.png')
plt.clf()

# avg fitness per generation
plt.plot(avg_fitness_vals_per_gen)
plt.ylabel('fitness')
plt.title('avg fitness per generation')
plt.savefig(f'results_plane_{run}/avg_fitness_per_gen.png')
plt.clf()

# fitness per robot
plt.plot(fitness_vals_all_robots)
plt.ylabel('fitness')
plt.title('fitness per robot')
plt.savefig(f'results_plane_{run}/fitness_per_robot.png')
plt.clf()

# correlation heat map
plt.figure(figsize=(30,30))
sns.heatmap(measures.corr(),
            vmin=-1,
            cmap='coolwarm',
            annot=True);
plt.savefig(f'results_plane_{run}/corr_matrix.png')
plt.clf()
