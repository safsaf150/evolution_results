import glob
import pandas as pd

gens = 20
data = []
for gen in range(0, gens):
    robots = glob.glob(f'selectedpop_{gen}/body_robot_*')
    for robot in robots:
        data.append([gen, int(robot.split('.')[0].split('_')[-1])])
df = pd.DataFrame(data, columns = ['generation', 'robot_id']) 
df.to_csv('fitness_vals.csv',index=False)

