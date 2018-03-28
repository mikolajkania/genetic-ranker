from elasticsearch import Elasticsearch

es = Elasticsearch()

res = es.search(index="articles", body={
    "query": {
        "match_all": {}
    }
})

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("[%(score)s] %(title)s" % {'title': hit['_source']['title'], 'score': hit['_score']})
