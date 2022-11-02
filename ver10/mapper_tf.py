#!/usr/bin/env python3
"""mapper.py"""

import sys
import pickle

l = 1
info = dict()


for line in sys.stdin:

    w = 1

    line = line.strip()
    
    words = line.split()
    
    for word in words:
        
        print(word, l, 1)
        w = w + 1
    
    info[l] = w-1   
    
    l = l + 1 
    

  
info['N'] = l-1


with open('file.pkl', 'wb') as file:
    pickle.dump(info, file)
