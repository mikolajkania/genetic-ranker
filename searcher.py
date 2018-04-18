from elasticsearch import Elasticsearch


class Searcher:
    es = Elasticsearch()

    def search(self, query, fields):
        res = self.es.search(index="articles", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "cross_fields",
                    "operator": "OR",
                    "fields": fields
                }
            }
        })

        print("For query '%(query)s' got %(hits)d hits:" % {'query': query, 'hits': res['hits']['total']})
        for hit in res['hits']['hits']:
            print("[%(score)s] [%(id)s] %(title)s" % {'score': hit['_score'],
                                                      'id': hit['_id'],
                                                      'title': hit['_source']['title']})

        return res['hits']['hits'][0]['_id']


def main():
    searcher = Searcher()
    searcher.search("privacy", ["title", "tags", "entities", "website", "type", "content_main", "content_additional"])


if __name__ == '__main__':
    main()
