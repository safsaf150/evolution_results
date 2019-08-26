import os
import glob
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

run = 1
path = f'plane_learning_{run}/data_fullevolution'
population = 5
gens = 5
offspring = 2
robots = (gens*offspring) + (population-offspring)

if not os.path.exists(f'learning_{run}'):
    os.mkdir(f'learning_{run}')
if not os.path.exists(f'learning_{run}/fitness_learn_all'):
    os.mkdir(f'learning_{run}/fitness_learn_all')
if not os.path.exists(f'learning_{run}/disp_vel_learn_all'):
    os.mkdir(f'learning_{run}/disp_vel_learn_all')

# collect learned fitness vals for all robots
learning_fitness_vals_all_robots = {}
for r_id in range(1, robots+1):
    file = open(glob.glob(f'{path}/fitness/fitness_learning_robot_{r_id}_*.txt')[0], 'r')
    fit_list = file.read().splitlines()
    learning_fitness_vals_all_robots[r_id] = [float(obj.split(' - ')[-1]) for obj in fit_list]
    file.close()

# plot learning fitness curves for each robot
for r_id in range(1, robots+1):
    plt.plot(np.arange(1, len(learning_fitness_vals_all_robots[r_id])+1), learning_fitness_vals_all_robots[r_id])
    plt.ylabel('fitness')
    plt.title(f'learning fitness robot {r_id}')
    plt.savefig(f'learning_{run}/fitness_learn_all/learn_fit_{r_id}.png')
    plt.clf()

# collect learned displacement velocity vals for all robots
learning_disp_vel_vals_all_robots = {}
for r_id in range(1, robots+1):
    files = glob.glob(f'{path}/descriptors/behavior_desc_robot_{r_id}_*.txt')
    dis_vel_vals = []
    for iteration in range(1, len(files)+1):
        file = open(glob.glob(f'{path}/descriptors/behavior_desc_robot_{r_id}_*_li_{iteration}.txt')[0], 'r')
        for line in file:
            measure, value = line.strip().split(' ')
            if measure == 'displacement_velocity':
                dis_vel_vals.append(float(value))
        file.close()
    learning_disp_vel_vals_all_robots[r_id] = dis_vel_vals
    
# plot learning displacement velocity curves for each robot
for r_id in range(1, robots+1):
    plt.plot(np.arange(1, len(learning_disp_vel_vals_all_robots[r_id])+1), learning_disp_vel_vals_all_robots[r_id])
    plt.ylabel('displacement velocity')
    plt.title(f'learning displacement velocity robot {r_id}')
    plt.savefig(f'learning_{run}/disp_vel_learn_all/learn_disp_vel_{r_id}.png')
    plt.clf()

# collect avg learning values per generation
all_gen_orig_learned = {}
origin_fit = {}
learn_fit = {}
robots_in_gen = dict([(i, []) for i in range(0, gens+1)])
for gen in range(0, gens):
    gen_orig_learned = []
    files_in_gen = glob.glob(f'{path}/fitness/fitness_learning_robot_*_gen_{gen}.txt')
    for file_n in files_in_gen:
        robot_id = int(file_n.split('robot_')[-1].split('_')[0])
        robots_in_gen[gen].append(robot_id)
        file = open(file_n, 'r')
        original_fitness = float(file.read().splitlines()[0].split(' - ')[1])
        file.close()
        file = open(f'{path}/fitness/fitness_robot_{robot_id}.txt', 'r')
        learned_fitness = float(file.read())
        file.close()
        gen_orig_learned.append([original_fitness, learned_fitness])
        origin_fit[robot_id] = original_fitness
        learn_fit[robot_id] = learned_fitness
    all_gen_orig_learned[gen] = gen_orig_learned


def calculate_delta(original, new):
    delta = 0
    if original < 0 or new < 0:
        delta = (abs(new) + abs(original)) / abs(original)
    else:
        delta = new / original
    if original > new:
        delta = -delta
    return delta

avg_delta_per_gen = []
for gen in range(0, gens):
    deltas = [calculate_delta(vals[0], vals[1]) for vals in all_gen_orig_learned[gen]]
    avg_delta_per_gen.append(np.mean(deltas))

org_list = sorted(origin_fit.items())
x_orig_list, y_orig_list = zip(*org_list)

lrn_list = sorted(learn_fit.items())
x_lrn_list, y_lrn_list = zip(*lrn_list) 

# plot learning deltas fitness all robots
plt.plot(x_orig_list, y_orig_list, label="original fitness values")
plt.plot(x_lrn_list, y_lrn_list, label="learned fitness values")
plt.legend(loc='upper right')
plt.title('original and learned fitness')
plt.savefig(f'learning_{run}/origin_learned_fitness_all_robots.png')
plt.clf()

plt.plot(np.arange(1, gens+1, 1), avg_delta_per_gen)
plt.xticks(range(1, gens+1))
plt.title('average delta value per generation')
plt.savefig(f'learning_{run}/average_delta_per_gen.png')
plt.clf()  

# collect avg displacement deltas per generation
all_orig_learned_displacement_gens = {}
origin_displacement = {}
learn_discplacement = {}
for gen in range(0, gens):
    disp_gen = []
    gen_orig_learned = []
    for r_id in robots_in_gen[gen]:
        origin_displ_vel = 0
        learned_displ_vel = 0
        file = open(f'{path}/descriptors/behavior_desc_robot_{r_id}_gen_{gen}_li_1.txt', 'r')
        for line in file:
            measure, value = line.strip().split(' ')
            if measure == 'displacement_velocity':
                origin_displ_vel = float(value)
        file.close()        
        file = open(f'{path}/descriptors/behavior_desc_robot_{r_id}.txt', 'r')
        for line in file:
            measure, value = line.strip().split(' ')
            if measure == 'displacement_velocity':
                learned_displ_vel = float(value)
        file.close()
        origin_displacement[r_id] = origin_displ_vel
        learn_discplacement[r_id] = learned_displ_vel
        disp_gen.append([origin_displ_vel, learned_displ_vel])
    all_orig_learned_displacement_gens[gen] = disp_gen

avg_delta_displacement_per_gen = []
for gen in range(0, gens):
    deltas = [calculate_delta(vals[0], vals[1]) for vals in all_orig_learned_displacement_gens[gen]]
    avg_delta_displacement_per_gen.append(np.mean(deltas))

org_list_d = sorted(origin_displacement.items())
x_orig_list_d, y_orig_list_d = zip(*org_list_d)

lrn_list_d = sorted(learn_discplacement.items())
x_lrn_list_d, y_lrn_list_d = zip(*lrn_list_d) 

# plot learning deltas displacement all robots
plt.plot(x_orig_list_d, y_orig_list_d, label="original displacement values")
plt.plot(x_lrn_list_d, y_lrn_list_d, label="learned displacement values")
plt.legend(loc='upper right')
plt.title('original and learned displacement velocity')
plt.savefig(f'learning_{run}/origin_learned_displacement_all_robots.png')
plt.clf()

plt.plot(np.arange(1, gens+1, 1), avg_delta_displacement_per_gen)
plt.xticks(range(1, gens+1))
plt.title('average delta displacement per generation')
plt.savefig(f'learning_{run}/average_delta_displacement_per_gen.png')
plt.clf()  


avg_orig_displ_per_gen = []
avg_lrn_displ_per_gen = []
for gen in range(0, gens):
    origin_d_g = []
    learn_d_g = []
    for r_id in robots_in_gen[gen]:
        origin_d_g.append(origin_displacement[r_id])
        learn_d_g.append(learn_discplacement[r_id])
    avg_orig_displ_per_gen.append(np.mean(origin_d_g))
    avg_lrn_displ_per_gen.append(np.mean(learn_d_g))

# plot avg original and learned displacement
plt.plot(np.arange(1, gens+1, 1), avg_orig_displ_per_gen, label="avg original displacement")
plt.plot(np.arange(1, gens+1, 1), avg_lrn_displ_per_gen, label="avg learned displacement")
plt.xticks(range(1, gens+1))
plt.legend(loc='upper right')
plt.title('avg original and learned displacement velocity per generation')
plt.savefig(f'learning_{run}/avg_origin_learned_displacement_per_gen.png')
plt.clf()
