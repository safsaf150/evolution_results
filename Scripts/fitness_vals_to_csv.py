import os
import pandas as pd 
  
gens =  int(sys.argv[1])

data = []

robots = (gens*50) + 50

# Create the pandas DataFrame 
for i in range(1, robots+1):
    file_name = f'fitness_robot_{i}.txt'
    if os.path.isfile(file_name):
        fit_file = open(file_name, 'r')
        fitness = fit_file.read()
        if fitness == 'None':
            fitness = None
        else:
            fitness = float(fitness)
        data.append([i, fitness])

df = pd.DataFrame(data, columns = ['id', 'fitness']) 
df.to_csv('fitness_vals.csv',index=False)