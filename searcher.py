from elasticsearch import Elasticsearch


class Searcher:
    es = Elasticsearch()

    def search(self, query, fields, weights=None):
        if weights is None:
            search_fields = fields
        else:
            if len(fields) != len(weights):
                raise ValueError('Fields & weights lengths should be equal!')
            search_fields = []
            for f, w in zip(fields, weights):
                search_fields.append(f + "^" + str(w))

        res = self.es.search(index="articles", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "cross_fields",
                    "operator": "OR",
                    "fields": search_fields
                }
            }
        })

        return [w['_id'] for w in res['hits']['hits']]


def main():
    searcher = Searcher()
    searcher.search("privacy", ["title", "tags", "entities", "website", "type", "content_main", "content_additional"])


if __name__ == '__main__':
    main()
