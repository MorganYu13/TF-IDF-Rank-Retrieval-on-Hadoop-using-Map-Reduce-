#!/bin/bash


echo "******************            TF with DocID                ***********************"

cat text.txt | sed "s/[^a-zA-Z ]//g" | tr "[:upper:]" "[:lower:]" | python3 mapper_tf.py | sort -k1,1 | python3 reducer_tf.py

echo "******************           IDF and keywords              ***********************"

cat text.txt | sed "s/[^a-zA-Z ]//g" | tr "[:upper:]" "[:lower:]" | python3 mapper_idf.py | sort -k1,1 | python3 reducer_idf.py

echo "***************   Final Keywords and their tf-idf values   ***********************"

cat text.txt | sed "s/[^a-zA-Z ]//g" | tr "[:upper:]" "[:lower:]" | python3 mapper_tf_idf.py | sort -k1,1 | python3 reducer_tf_idf.py > tf_idf.txt

cat tf_idf.txt

cat tf_idf.txt > tf_idf.csv
