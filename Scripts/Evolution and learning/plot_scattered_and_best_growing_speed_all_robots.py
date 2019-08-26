import os
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


os.mkdir('generational')
os.mkdir('all_scattered_speed')
os.mkdir('best_yet_speed')

robots = 503
gens = math.floor((robots / 50) - 1)

origin_speeds = {}
final_speeds = {}
learned_speeds = {}

for r_id in range(1, robots+1):
    file = open(f'descriptors/behavior_desc_robot_{r_id}.txt')
    displacement = None
    descriptions = file.read().splitlines()
    file.close()
    
    try:
        displacement = [float(displacement.split(' ')[-1]) for displacement in descriptions if 'displacement_velocity ' in displacement][0]
    except:
        pass
        
    final_speeds[r_id] = displacement if displacement < 10 else 0
    

for r_id in range(1, robots+1):
    gen = 1 if r_id < 101 else math.ceil((r_id-50)/50)
    file = open(f'descriptors/behavior_desc_robot_{r_id}_gen_{gen-1}_li_1.txt')
    displacement = None
    descriptions = file.read().splitlines()
    file.close()
    
    try:
        displacement = [float(displacement.split(' ')[-1]) for displacement in descriptions if 'displacement_velocity ' in displacement][0]
    except:
        pass
        
    origin_speeds[r_id] = displacement

begin = 0
end = 100
for gen in range(0, gens):
    plt.plot(list(origin_speeds.keys())[begin:end], list(origin_speeds.values())[begin:end])
    plt.plot(list(final_speeds.keys())[begin:end], list(final_speeds.values())[begin:end])
    plt.savefig(f'generational/learned_and_original_speed_gen_{gen+1}.png')
    plt.clf()
    
    begin += 50 if gen > 0 else 100
    end += 50
    
for r_id in range(1, robots+1):
    print(r_id)
    l_speeds = []
    gen = 1 if r_id < 101 else math.ceil((r_id-50)/50)
    for iteration in range(1, 525):
        try:
            file = open(f'descriptors/behavior_desc_robot_{r_id}_gen_{gen-1}_li_{iteration}.txt')
            displacement = None
            descriptions = file.read().splitlines()
            file.close()
            
            try:
                displacement = [float(displacement.split(' ')[-1]) for displacement in descriptions if 'displacement_velocity ' in displacement][0]
            except:
                pass
                
            l_speeds.append(displacement)
            
        except:
            pass
        
    learned_speeds[r_id] = l_speeds
    
for r_id in range(1, robots+1):
    y = learned_speeds[r_id]
    if len(y) > 1:
        x = np.arange(1, len(y)+1)
        plt.scatter(x, y)
        min_val = min(y)
        max_val = max(y)
        plt.ylim(min_val, max_val)
        plt.savefig(f'all_scattered_speed/{r_id}.png')
        plt.clf()    
        
        
best_yet_robots = {}
for i in range(1, robots+1):
    best_yet = []
    indexes = []
    l_vals = learned_speeds[i]
    for j in range(len(l_vals)):
        if not best_yet or all(i < l_vals[j] for i in best_yet):
            best_yet.append(l_vals[j])
            indexes.append(j+1)
    best_yet.append(max(best_yet))
    indexes.append(len(l_vals)+1)
    best_yet_robots[i] = best_yet, indexes
    
    
for i in range(1, robots+1):
    y, x = best_yet_robots[i]
    # meters to centimeters speed
    y = [i * 100 for i in y]
    if len(y) > 2:
        plt.fill_between(x, y)
        min_val = min(y) if min(x) < 0 else 0
        max_val = max(y)*1.5 if max(y) >= 0 else max(y)
        plt.ylim(min_val, max_val)
        plt.savefig(f'best_yet_speed/{i}.png')
        plt.clf()


avg_original_speed_per_gen = {}
avg_learned_speed_per_gen = {}

for gen in range(1, gens+1):
    all_origin_speeds = []
    all_learned_speeds = []
    gen_ids = np.arange(1,101) if gen == 1 else np.arange(gen*50+1, gen*50+51)
    
    for r_id in gen_ids:
        all_origin_speeds.append(origin_speeds[r_id])
        all_learned_speeds.append(final_speeds[r_id])
    avg_original_speed_per_gen[gen] = np.mean(all_origin_speeds)
    avg_learned_speed_per_gen[gen] = np.mean(all_learned_speeds)

# plot avg learned and original
plt.plot(avg_original_speed_per_gen.keys(), avg_original_speed_per_gen.values())
plt.plot(avg_learned_speed_per_gen.keys(), avg_learned_speed_per_gen.values())
plt.savefig('avg/avg_learned_original_speed.png')
plt.clf()

end_learn = []
for r_id in range(1, robots+1):
    speeds, indexes = best_yet_robots[r_id]
    end_learn.append(indexes[-2])
    
end_learn = [x for x in end_learn if x != 1]
mean = np.mean(end_learn)
median = np.median(end_learn)
st_dev = np.std(end_learn)


robots_signif = []
not_signif = []
most_learned_id = 0
most_learned_diff = 0

for rid in range(1, robots+1):
    o = origin_speeds[rid]
    l = final_speeds[rid]
    diff = l-o
    
    if diff > most_learned_diff:
        most_learned_diff = diff
        most_learned_id = rid
    
    if not diff >  0.00001:
        not_signif.append(rid)
    else:
        print(diff)
        robots_signif.append(rid)

#plot significanly learned robots only
for i in range(1, robots+1):
    y, x = best_yet_robots[i]
    # meters to centimeters speed
    y = [i * 100 for i in y]
    if len(y) > 2 and i not in not_signif:
        plt.fill_between(x, y)
        min_val = min(y) if min(x) < 0 else 0
        max_val = max(y)*1.5 if max(y) >= 0 else max(y)
        plt.ylim(min_val, max_val)
        plt.savefig(f'best_yet_speed_s/{i}.png')
        plt.clf()