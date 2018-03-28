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
    print("For query '%(query)s' got %(hits)d Hits:" % {'query': query, 'hits': res['hits']['total']})
    for hit in res['hits']['hits']:
        print("[%(score)s] %(title)s" % {'title': hit['_source']['title'], 'score': hit['_score']})
    print('\n')


search("privacy facebook")
search("privacy")
search("trump cambridge")
search("trump")
search("guardian")
