#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys

current_doc_id = 0
current_tfidf = 0
doc_id = None


for line in sys.stdin:
     
    line = line.strip()

     
    doc_id, tfidf = line.split(' ')

     
    try:
        doc_id = int(doc_id)
        tfidf = float(tfidf)
    except ValueError:
        continue

     
    if current_doc_id == doc_id:
        current_tfidf += tfidf
    else:
        if current_doc_id:
            current_tfidf = "%.4f" % round(current_tfidf, 4)
            print (current_tfidf, 'is the cummulative tf-idf for the Doc ID', current_doc_id)
            
        current_doc_id = doc_id
        current_tfidf = tfidf

 
if current_doc_id == doc_id:
    current_tfidf = "%.4f" % round(current_tfidf, 4)
    print (current_tfidf, 'is the cummulative tf-idf for the Doc ID', current_doc_id)
