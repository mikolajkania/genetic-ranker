from elasticsearch import Elasticsearch

es = Elasticsearch()


def search(query):
    res = es.search(index="articles", body={
        "query": {
            "multi_match": {
                "query": query,
                "type": "cross_fields",
                "operator": "OR",
                "fields": ["title", "tags", "entities", "website", "type", "content_main", "content_additional"]
            }
        }
    })
    print("For query '%(query)s' got %(hits)d hits:" % {'query': query, 'hits': res['hits']['total']})
    for hit in res['hits']['hits']:
        print("[%(score)s] [%(id)s] %(title)s" % {'score': hit['_score'], 'id': hit['_id'] ,'title': hit['_source']['title']})
    print('\n')


search("privacy facebook")
search("privacy")
search("facebook")
search("cambridge analytica")
search("trump cambridge")
search("trump facebook")
search("guardian article")
search("tesla article")
search("tesla facebook stock market")
search("blog facebook data breach")
