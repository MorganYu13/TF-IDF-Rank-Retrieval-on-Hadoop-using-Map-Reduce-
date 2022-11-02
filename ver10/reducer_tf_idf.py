#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys
import pickle

current_word = None
current_doc_id = 0
current_count = 0
word = None



import time
time.sleep(2)
  
with open('file.pkl', 'rb') as file:
      
    info = pickle.load(file)
    #print('-- Total Docs -->', info['N'])
    
    
with open('word_idf.pkl', 'rb') as file:
      
    word_idf = pickle.load(file)



for line in sys.stdin:
     
    line = line.strip()

     
    word, doc_id, count = line.split(' ')

    try:
        doc_id = int(doc_id)
        count = int(count)
    except ValueError:
        continue
     
    if current_word == word and current_doc_id == doc_id:
        current_count += count
    else:
        if current_word:
            print ( current_word, current_doc_id, round(current_count/info[current_doc_id]*word_idf[current_word], 4), sep=',')
            
        current_count = count
        current_doc_id = doc_id
        current_word = word

 
if current_word == word:
    print (current_word, current_doc_id, round(current_count/info[current_doc_id]*word_idf[current_word],4), sep=',')
   
    
    

    
    
    
