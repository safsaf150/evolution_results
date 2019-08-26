import numpy as np
import PIL
import os
from itertools import combinations 
f_name = 'pairs_40'

columns = ['branching', 'limbs', 'extremities', 'extensiveness', 'coverage', 'joints', 
         'proportion', 'width', 'length', 'absolute_size', 'symmetry', 'active_hinges_count', 'length_of_limbs']

combos_cols = list(combinations(columns, 2))

os.mkdir(f_name)
for combo in combos_cols:
    f,s = combo[0],combo[1]
    file_one = f'{f}_{s}_gen_1-3.png'
    file_two = f'{f}_{s}_gen_38-40.png'
    if os.path.isfile(file_one) and os.path.isfile(file_one):
        list_im = [file_one, file_two]

        imgs    = [ PIL.Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        
        # save that beautiful picture
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save(f'{f_name}/{f}_{s}_combo.png')
