#!/usr/bin/env python3
"""mapper.py"""

import sys
import pickle


l = 1
info = dict()


for line in sys.stdin:

    line = line.strip()
    
    words = line.split()
    
    for word in words:
        
        if(word != ""):
            print(word.lower(), l, 1)
    
    l = l + 1 
    
info['N'] = l-1


with open('file.pkl', 'wb') as file:
    pickle.dump(info, file)
