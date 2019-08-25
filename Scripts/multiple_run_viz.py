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
    
    
    avg_runs_fitness.append(avg_fitness_vals_per_gen)
    avg_runs_displacement.append(d_avg_vel_vals_per_gen)
    
    # avg displacement velocity per generation
#    plt.figure(figsize=(10,10))
    in_cm = [x * 100 for x in d_avg_vel_vals_per_gen]
    plt.plot(in_cm)
    plt.ylabel('Speed (cm/s)')
    plt.xlabel('Generation')
#    plt.title('avg displacement velocity per generation')
    plt.savefig(f'results_plane_{run}/avg_displacement_per_gen.png', bbox_inches='tight')
    plt.clf()
    
#    # displacement velocity per robot
#    plt.plot(d_vel_vals_all_robots)
#    plt.ylabel('displacement velocity')
#    plt.title('displacement velocity per robot')
#    plt.savefig(f'results_plane_{run}/displacement_per_robot.png', bbox_inches='tight')
#    plt.clf()
    
    # avg fitness per generation
    plt.plot(avg_fitness_vals_per_gen)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    #plt.title('avg fitness per generation')
    plt.savefig(f'results_plane_{run}/avg_fitness_per_gen.png', bbox_inches='tight')
    plt.clf()
    
#    # fitness per robot
#    plt.plot(fitness_vals_all_robots)
#    plt.ylabel('Fitness')
#    plt.title('fitness per robot')
#    plt.savefig(f'results_plane_{run}/fitness_per_robot.png', bbox_inches='tight')
#    plt.clf()
    
    # correlation heat map
#    plt.figure(figsize=(30,30))
    sns.heatmap(measures.corr(),
                vmin=-1,
                cmap='coolwarm',
                annot=True);
    plt.savefig(f'results_plane_{run}/corr_matrix.png', bbox_inches='tight')
    plt.clf()

if not os.path.exists(f'results_plane_avg'):
    os.mkdir(f'results_plane_avg')


all_runs_avg_displacement = np.array(avg_runs_displacement).mean(axis=0)
all_runs_avg_std = np.array(avg_runs_displacement).std(axis=0)
nine_runs_displacement = avg_runs_displacement[1:]
nine_runs_avg_std = np.array(nine_runs_displacement).std(axis=0)
all_runs_avg_fitness = np.array(avg_runs_fitness).mean(axis=0)

# avg fitness per generation avg all runs
#plt.figure(figsize=(10,10))
plt.plot(all_runs_avg_displacement*100)
plt.xlabel('Generation')
plt.ylabel('Speed (cm/s)')
#plt.title('avg displacement per generation')
plt.savefig(f'results_plane_avg/all_run_avg_displacement_per_gen.png', bbox_inches='tight')
plt.clf()

# avg displacement per generation avg all runs
plt.plot(all_runs_avg_fitness)
plt.xlabel('Generation')
plt.ylabel('Fitness')
#plt.title('avg fitness per generation')
plt.savefig(f'results_plane_avg/all_run_avg_fitness_per_gen.png', bbox_inches='tight')
plt.clf()

# avg stf per generation avg all runs
axes = plt.gca()
axes.set_ylim([0, .05])
plt.plot(all_runs_avg_std)
plt.xlabel('Generation')
plt.ylabel('Standard deviation')
#plt.title('avg fitness per generation')
plt.savefig(f'results_plane_avg/avg_std_all_runs.png', bbox_inches='tight')
plt.clf()

# avg stf per generation avg all runs
axes = plt.gca()
axes.set_ylim([0, .05])
plt.plot(nine_runs_avg_std)
plt.xlabel('Generation')
plt.ylabel('Standard deviation')
#plt.title('avg fitness per generation')
plt.savefig(f'results_plane_avg/avg_std_9_runs.png', bbox_inches='tight')
plt.clf()
