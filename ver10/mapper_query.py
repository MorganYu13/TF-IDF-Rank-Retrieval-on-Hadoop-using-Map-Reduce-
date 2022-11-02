#!/usr/bin/env python3
"""mapper.py"""

import sys

with open('queries.txt', 'r') as f:
	while True:
		line = f.readline()
		if not line:
			break
			
		query = line.strip()
		query_keys = query.split()
		
		query_keys = set(query_keys)
		
		for sys_line in sys.stdin:
			sys_line = sys_line.strip()
			word, doc_id, tfidf = sys_line.split(',')
			
			
			if word in query_keys:
				print(doc_id, tfidf)
