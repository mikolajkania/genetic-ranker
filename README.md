# Genetic Ranker
Genetic Ranker is a framework using power of genetic algorithms to find optimal search weights for ElasticSearch or Solr queries.

## The reason

Finding optimal search weights for fields is long-lasting and ungrateful process. Imagine an index with millions of documents, every with tens of fields, and hundred of queries that should be tested to ensure how good actual configuration is. Your job is to determine how important are particular fields. It can take a lifetime. 

I [wrote a post](http://itblues.pl/2018/06/15/Genetic-ranker-a-genetic-algorithm-framework/)  about that on my blog, take a look if you need more information about this process. 

## Why genetic algorithm?

Firstly, it is easy to *define problem as set of numeric weights* that can be altered during processing. Mutation, crossover & reproduction parts of the algorithm can easily be done on numbers. 

Secondly, genetic algorithms are able to *preserve solutions that are promising*, even without actual understanding of a problem. Better species (individuals) will be kept and be an ancestors for even better ones.

Thirdly, due to mutation & crossover parts, algorithm *adds a bit of randomness to the process*. It may help to find the best answer even if actual is good. 

More on that, again, [here](http://itblues.pl/2018/06/15/Genetic-ranker-a-genetic-algorithm-framework/).

## How to run

To start GeneticRanker you need to run a ranker.py file. Project contains all data required to demonstrate simple use case.

## Basic configuration

In ranker.py you should define how many fields you want to use (*gene_size* in *Ranker*). Then specify those fields in *Evaluator* class (*fields*).

In queries.csv you need to specify use cases you want to test. The format is:

<pre>[query],[document_id]:[expected_position]:[good_enough_position]</pre>

In *properties.ini* you can define which search engine you want to use: Elasticsearch or Solr. Queries should be defined in *essearcher.py* and *solrsearcher.py* respectively.
 
## Test it yourself
 
 Imagine you are a search engineer who have to find optimal weights for fields upon which the queries are run. The only things you have is file *queries.csv*, containing queries, and documents in the index. Before running GeneticRanker take a while to read these csv file and analyze documents from *queries-es.txt*. 
 
 There are only 8 documents and 10 queries but I guarantee that you can spend a while on this task.
 
 In *data* directory there are files containing documents. You can use any Elasticsearch and Solr ways to index them, but for the former I used Postman tool and for the later - Solr admin panel.
 
 Having the server up and running should be enough to run a script and see the results.

## Used Python libs

<pre>deap
elasticsearch
pysolr</pre>

You should check their licenses and decide wheter you can use it your software. 

## The end

Every use case may need alteration of genetic algorithm values or algorithm itself, but proposed configuration should be a good starting point. Happy using!