import os
import glob
import math

import numpy as np
import matplotlib.pyplot as plt


def calculate_delta(original, new):
    delta = 0
    if original < 0 or new < 0:
        delta = (abs(new) + abs(original)) / abs(original)
    else:
        delta = new / original
    if original > new:
        delta = -delta
    return delta


os.mkdir('best_yet')
os.mkdir('avg')
os.mkdir('all_scattered')

robots = 503
gens = math.floor((robots / 50) - 1)

fitness_vals = {}
learned_vals = {}

not_learned = []


for i in range(1, robots+1):
    file = open(f'fitness/fitness_robot_{i}.txt')
    fitness = file.read()
    file.close()
    fitness_vals[i] = float(fitness)
    glob.glob(f'fitness/fitness_learning_robot_{i}_gen_*.txt')[0]

for i in range(1, robots+1):
    path = glob.glob(f'fitness/fitness_learning_robot_{i}_gen_*.txt')[0]
    file = open(path)
    fit_list = file.read().splitlines()
    fitness_values = [float(obj.split(' - ')[-1]) for obj in fit_list]
    learned_vals[i] = fitness_values
    if len(fitness_values) == 1:
        not_learned.append(i)

original = {k:v[0] for k, v in learned_vals.items()}
post_learning = fitness_vals

for i in range(1, robots+1):
    if i not in not_learned:
        y = learned_vals[i]
        x = np.arange(1, len(y)+1)
        plt.scatter(x, y)
        min_val = min(y)
        max_val = max(y)
        plt.ylim(min_val, max_val)
        plt.savefig(f'all_scattered/{i}.png')
        plt.clf()
        
best_yet_robots = {}
for i in range(1, robots+1):
    best_yet = []
    indexes = []
    l_vals = learned_vals[i]
    for j in range(len(l_vals)):
        if not best_yet or all(i < l_vals[j] for i in best_yet):
            best_yet.append(l_vals[j])
            indexes.append(j+1)
    best_yet.append(max(best_yet))
    indexes.append(len(l_vals)+1)
    best_yet_robots[i] = best_yet, indexes
    
for i in range(1, robots+1):
    if i not in not_learned and len(best_yet_robots[i]) == 2:
        y, x = best_yet_robots[i]
        plt.fill_between(x, y)
        min_val = min(y)
        max_val = max(y)*1.5 if max(y) >= 0 else max(y)
        plt.ylim(min_val, max_val)
        plt.savefig(f'best_yet/{i}.png')
        plt.clf()
        

avg_original_fitness_per_gen = {}
avg_learned_fitness_per_gen = {}


for gen in range(1, gens+1):
    all_origin_fitness = []
    all_learned_fitness = []
    gen_ids = np.arange(1,101) if gen == 1 else np.arange(gen*50+1, gen*50+51)
    for r_id in gen_ids:
        all_origin_fitness.append(learned_vals[r_id][0])
        all_learned_fitness.append(fitness_vals[r_id])
    avg_original_fitness_per_gen[gen] = np.mean(all_origin_fitness)
    avg_learned_fitness_per_gen[gen] = np.mean(all_learned_fitness)


delta_generational = [calculate_delta(avg_original_fitness_per_gen[i], avg_learned_fitness_per_gen[i]) for i in set(avg_original_fitness_per_gen) & set(avg_learned_fitness_per_gen)]


# plot avg learned and original
plt.plot(avg_original_fitness_per_gen.keys(), avg_original_fitness_per_gen.values())
plt.plot(avg_learned_fitness_per_gen.keys(), avg_learned_fitness_per_gen.values())
plt.savefig('avg/avg_learned_original_fitness.png')
plt.clf()

best_robots_per_gen_pre_learn = []
best_robots_per_gen_post_learn = []
largest_delta_robot_per_gen = []

for gen in range(1, gens+1):
    best_in_gen_pre_l_id = -1
    best_in_gen_post_l_id = -1
    best_delta_id = -1
    
    fit_pre = -1
    fit_post = -1
    delta = -1
    
    gen_ids = np.arange(1,101) if gen == 1 else np.arange(gen*50+1, gen*50+51)
    #original, post_learning
    for r_id in gen_ids:
        o = original[r_id]
        p = post_learning[r_id]
        d = calculate_delta(o, p)
        
        if o > fit_pre:
            fit_pre = o
            best_in_gen_pre_l_id = r_id
        if p > fit_post:
            fit_post = p
            best_in_gen_post_l_id = r_id
        if d > delta:
            delta = d
            best_delta_id = r_id
    
    best_robots_per_gen_pre_learn.append({best_in_gen_pre_l_id:fit_pre})
    best_robots_per_gen_post_learn.append({best_in_gen_post_l_id:fit_post})
    largest_delta_robot_per_gen.append({best_delta_id:delta})

