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
        print("[%(score)s] %(title)s" % {'title': hit['_source']['title'], 'score': hit['_score']})
    print('\n')


search("privacy facebook")  # first is not about facebook
search("privacy")       # ok+-
search("trump cambridge")   # ok
search("trump")     # facebook stock nothing to do with trump
search("guardian article")  # website below false mention
search("tesla")
