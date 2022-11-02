#!/bin/bash


echo "***********          DocId most fitting with the query          ***********"

cat tf_idf.txt | python3 mapper_query.py | sort -k1,1 | python3 reducer_query.py | sort -n -r
