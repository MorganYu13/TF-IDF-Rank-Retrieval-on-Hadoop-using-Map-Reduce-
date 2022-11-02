#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys
import pickle
import math

current_word = None
current_doc_id = 0
current_count = 0
word = None


word_idf = dict()


import time
time.sleep(2)
  
with open('file.pkl', 'rb') as file:
      
    info = pickle.load(file)
    print('-- Total Docs -->', info['N'])



for line in sys.stdin:
     
    line = line.strip()

     
    word, doc_id, count = line.split(' ')

    try:
        doc_id = int(doc_id)
        count = int(count)
    except ValueError:
        continue
     
    if current_word == word:
        current_count += count
    else:
        if current_word:
            print (current_word, round(math.log(info['N']/current_count), 4))
            word_idf[current_word] = round(math.log(info['N']/current_count), 4)
        current_count = count
        current_doc_id = doc_id
        current_word = word

 
if current_word == word:
    print (current_word, round(math.log(info['N']/current_count), 4))
    word_idf[current_word] = round(math.log(info['N']/current_count), 4)
    

with open('word_idf.pkl', 'wb') as file:
    pickle.dump(word_idf, file)
    
    
    
    
