# Ranked Document Retrieval using tf-idf Computations using Map Reduce on Hadoop 

This project implements a tf-idf Ranked Retrieval of Documents using Map Reduce on Hadoop. This in total contains four MR jobs, each for tf, idf, tf-idf and finally the query system. 
<br>*Dataset:-*  [*Kaggle Dataset Link - Long Text Document with all reviews*](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews?select=train.ft.txt.bz2)

## Example Computation
We'll be seeing how documents get ranked using tf-idf and further query processing. For demo purposes we use these as example documents - 
```
Corpus:

Doc ID 1 - The laptop isn't that great. So ANNOYING!!!!
Doc ID 2 - The bag which came along with the laptop is ~~$ok. 
Doc ID 3 - The mobile is great. But overheating is so annoying  >>:((
Doc ID 4 - The mobile is ok ok. 
Doc ID 5 - The bag and mobile combo is epic!!
```
**Input** 
<br>We give in a query for example = 
```
query:

great laptop
```

**Output**
<br>We get a resorted list of documents (only the ones which have the query terms), top most document being the most relevant and closest to the query, ranging from top most relevancy to least. 

```
sorted list of Docs according to query

Doc ID 1 - The laptop isn't that great. So ANNOYING!!!!
Doc ID 3 - The bag which came along with the laptop is ~~$ok. 
Doc ID 2 - The mobile is great. But overheating is so annoying  >>:((
```

## Meaning of [tf - idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
As per wikipedia
> In [information retrieval](https://en.wikipedia.org/wiki/Information_retrieval "Information retrieval"), **tf–idf** (also **TF*IDF**, **TFIDF**, **TF–IDF**, or **Tf–idf**), short for **term frequency–inverse document frequency**, is a numerical statistic that is intended to reflect how important a word is to a [document](https://en.wikipedia.org/wiki/Document "Document") in a collection or [corpus](https://en.wikipedia.org/wiki/Text_corpus "Text corpus").
> 
The formula used is:- 
![TF-IDF: Can It Really Help Your SEO?](https://cdn.searchenginejournal.com/wp-content/uploads/2019/10/screenshot-1.png)

*Note: tf-idf is also robust and immune to stop words, and negatively penalizes weights for stop words, making it almost nullify the use of removal of stop words. Due to which we do NOT remove stop words as a preprocessing step.* 

## Task 0 - Setup Files 
When running this first, we want to check if we are getting the code to run on a smaller corpus first, this is easier to debug and get faster results. 
<br>For which
<br>**Step 1: Set up text.txt file** 
<br>If you have cloned the repo, this can be avoided. 
<br>But ensure that the [text.txt](https://github.com/MorganYu13/TF-IDF-Rank-Retrieval-on-Hadoop-using-Map-Reduce-/blob/main/ver10/text.txt "text.txt") file contains 
```
The laptop isn’t that great. So ANNOYING!!!
The bag which came along with the laptop is ~~$ok.
The mobile is great. But overheating is so annoying >>:((
```

**Step 2: Set up of query.txt file**
<br>If you have cloned the repo, this can be avoided. 
<br>But ensure that the [query.txt](https://github.com/MorganYu13/TF-IDF-Rank-Retrieval-on-Hadoop-using-Map-Reduce-/blob/main/ver10/query.txt "query.txt") file contains 
```
great laptop
```
## Task 1 - Data Preprocessing 

**step 1** :- Save the Reviews dataset from the kaggle link as [text1.txt](https://github.com/MorganYu13/TF-IDF-Rank-Retrieval-on-Hadoop-using-Map-Reduce-/blob/main/ver10/text1.txt "text1.txt"). For the purpose of easy processing we are using the test.txt file. Convert the input file to its cleaned form using bash script
```bash
      cat text.txt | sed "s/[^a-zA-Z ]//g" | tr "[:upper:]" "[:lower:]" > text1.txt
```

This converts the above lines to: 
```
the laptop isnt that great so annoying
the bag which came along with the laptop is ok
the mobile is great but overheating is so annoying
```

## Task 2 - Hadoop 
-  Clone the repo and `cd` to the folder of ver10
- Give permissions to all py files. 
```bash
 chmod u+x mapper_tf.py
 chmod u+x reducer_tf.py
 chmod u+x mapper_idf.py
 chmod u+x reducer_idf.py
 chmod u+x mapper_tf_idf.py
 chmod u+x reducer_tf_idf.py
 chmod u+x mapper_query.py
 chmod u+x reducer_query.py
```  
- Now we feed this text1.txt to hadoop. For hadoop start up, start the daemons, namenodes and datanodes using `start-all.sh`  in `/hadoop-3.2.2/sbin`. We will be using hadoop 3.2.2. Do follow the sbin folder as per the Hadoop Folder Section.
- Make sure the mapred-site.xml is set properly, follow this to set the mapred-site.xml. 
 [HPE ref guide for Mapred_site.xml](https://docs.datafabric.hpe.com/70/ReferenceGuide/mapred-site.xml.html)
 [Github Mapred_site.xml](https://github.com/hanborq/hadoop/blob/master/example-confs/conf.secure/mapred-site.xml)
[Cloudera Security Ref Mapred_site.xml](https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.0/security-reference/content/kerberos_nonambari_mapred_site_xml.html)
[Apache Documentation Mapred_site.xml](https://hadoop.apache.org/docs/r2.7.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml)


- `jps` to confirm all nodes running. Make sure you get: 
```bash
	5392 Jps
	3427 NameNode
	4133 NodeManager
	3557 DataNode
	3751 SecondaryNameNode
	3996 ResourceManager
```                
- Now make a folder in HDFS using 
```bash
	hdfs dfs -mkdir /ver1_any_folder_name
```
- Confirm using `hdfs dfs -ls /`
- Now put the text1.txt in the HDFS folder (Make sure the paths are all corrected to your system)
```bash
	hdfs dfs -put /home/ver10/text1.txt hdfs://127.0.0.1:9000/ver1
```
- Confirm using `hdfs dfs -cat /ver1/text1.txt`
- `cd` back to the ver10 folder

## Task 3 - tf calculation
Now we will run the map reduce files, first for tf python. 
- run hadoop map reduce on all files (TF)
```bash
	hadoop jar /home/hadoop-3.2.2/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar   \
	-mapper "/home/ver10/mapper_tf.py" \
	-reducer "/home/ver10/reducer_tf.py" \
	-input /ver1/text1.txt     \
	-output /ver1/output1
```
- To view the output 
```bash
	hdfs dfs -cat /ver1/output1/part-00000
```

```
-- Total Docs --> 3 

2 Doc: along 0.1 
1 Doc: annoying 0.14 
3 Doc: annoying 0.11 
2 Doc: bag 0.1 
3 Doc: but 0.11 
2 Doc: came 0.1 
1 Doc: great 0.14 
3 Doc: great 0.11 
2 Doc: is 0.1 
3 Doc: is 0.22 
1 Doc: isnt 0.14 
1 Doc: laptop 0.14 
2 Doc: laptop 0.1 
3 Doc: mobile 0.11 
2 Doc: ok 0.1 
3 Doc: overheating 0.11 
1 Doc: so 0.14 
3 Doc: so 0.11 
1 Doc: that 0.14 
1 Doc: the 0.14 
2 Doc: the 0.2 
3 Doc: the 0.11 
2 Doc: which 0.1 
2 Doc: with 0.1
```

## Task 4 - idf calculation

Now we will run the idf map reduce files
- run hadoop map reduce on all files (IDF)
```bash
hadoop jar /home/pes2ug19cs041/hadoop-3.2.2/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar \
-mapper "/home/ver10/mapper_idf.py" \
-reducer "/home/ver10/reducer_idf.py" \
-input /ver1/text1.txt \
-output /ver1/output2
```
- To view the output 
```bash
hdfs dfs -cat /ver1/output2/part-00000
```

``` 
-- Total Docs --> 3 

along 1.0986 
annoying 0.4055 
bag 1.0986 
but 1.0986 
came 1.0986 
great 0.4055 
is 0.0 
isnt 1.0986 
laptop 0.4055 
mobile 1.0986 
ok 1.0986 
overheating 1.0986 
so 0.4055 
that 1.0986 
the -0.2877 
which 1.0986 
with 1.0986
```

## Task 5 - tf-idf Combination calculation 

Now we will run the tf-idf map reduce files
- run hadoop map reduce on all files (TF-IDF) 
```bash
hadoop jar /home/pes2ug19cs041/hadoop-3.2.2/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar \
-mapper "/home/pes2ug19cs041/Distributed_Systems/ver10/mapper_tf_idf.py" \
-reducer "/home/pes2ug19cs041/Distributed_Systems/ver10/reducer_tf_idf.py" \
-input /ver4/text1.txt \
-output /ver4/output3 
```

- To view the output 
```bash
hdfs dfs -cat /ver1/output3/part-00000
```

After calculating tf and idf, we multiply for each tf and idf for each term, for each document. This will give us a measure of 
<term, doc_id, tf-idf>
<br>Using this, we can figure out what terms have what weight in which document. 
```
along,2,0.1099 
annoying,1,0.0579 
annoying,3,0.0451 
bag,2,0.1099 
but,3,0.1221 
came,2,0.1099 
great,1,0.0579 
great,3,0.0451 
is,2,0.0 
is,3,0.0 
isnt,1,0.1569 
laptop,1,0.0579 
laptop,2,0.0406 
mobile,3,0.1221 
ok,2,0.1099 
overheating,3,0.1221 
so,1,0.0579 
so,3,0.0451 
that,1,0.1569 
the,1,-0.0411 
the,2,-0.0575 
the,3,-0.032 
which,2,0.1099 
with,2,0.1099
```
## Task 6 - query processing 
Given our query will be "great laptop", as  a result of having to search for some good reviews, what we will be doing is have a cumulative sum of the word great and laptop in each docs. And then based on these sums we have a final sort of the docs which contain the words, with the top most doc being the most relevant doc with respect to the query. 
<br>
<br>For example: 
<br>
```
query: 
		"great laptop"
corpus:
		the laptop isnt that great so annoying  
		the bag which came along with the laptop is ok  
		the mobile is great but overheating is so annoying

Docs and presence of query terms: 
		doc 1 has the terms {laptop, great}
		doc 2 has the terms {laptop}
		doc 3 has the terms {great}

therefore we do: 
		tf-idf(doc1_laptop) + tf-idf(doc1_great)  = total relevancy score for doc 1
		tf-idf(doc2_laptop)                       = total relevancy score for doc 2
		tf-idf(doc3_great)                        = total relevancy score for doc 3
```
<br>
 We see that in the output we get: 

```
*********** DocId most fitting with the query ***********
		 0.1158 is the cummulative tf-idf for the Doc ID 1 
		 0.0451 is the cummulative tf-idf for the Doc ID 3 
		 0.0406 is the cummulative tf-idf for the Doc ID 2
```

Therefore Doc 1 got the highest score, since both laptop and great was present, the other two almost having the same score since only one of the terms (laptop/great) was present in those Docs. 
<br>
<br>
<br>
## Limitations 
- **Context of the query is not taken into consideration**: As in the previous example, we wanted to search for the review with a good review, hence we took the query "great laptop". The returned document (Doc1) with the highest relevancy was infact a negative review. Hence this method can be used for raw keywords, ie. keywords which do not hold any meaning. 
- **Weightage of Words are not taken into consideration**: We would, by default, want to keep a higher weight for laptop over great, since we want good **laptop** reviews, not reviews which are in general **great**. Therefore such kind of weightage is not taken into consideration. 

## Future Additions
- The limitations above mentioned can be fixed by adding a feature by incorporating a weight parameter in the cumulative relevancy score calculation for each doc. By manually setting weights while taking in the query input, and multiplying the weight for each query with the tf-idf can help with this. 
- Example:- where weight for laptop is kept much higher than for great, the docs which have Laptops will be shown first. 
```
	wt(laptop)*tf-idf(doc1_laptop) + wt(great)*tf-idf(doc1_great)  = total relevancy score for doc 1
        wt(laptop)*tf-idf(doc2_laptop)                                 = total relevancy score for doc 2
        wt(great)tf-idf(doc3_great)                                    = total relevancy score for doc 3
```
- This was run on a standalone Hadoop Cluster only. 

## Running locally on python
Given are two bash files. tf-idf part can be done by running the [run_task1.sh](https://github.com/MorganYu13/TF-IDF-Rank-Retrieval-on-Hadoop-using-Map-Reduce-/blob/main/ver10/run_task1.sh "run_task1.sh") first. `cd` to the ver10 folder and then run `./run_task1.sh`. For the second query processing part, this can be done by running the [run_task2.sh](https://github.com/MorganYu13/TF-IDF-Rank-Retrieval-on-Hadoop-using-Map-Reduce-/blob/main/ver10/run_task2.sh "run_task2.sh"). Run by using `./run_task2.sh`. 


