import pysolr


class SolrSearcher:
    solr = pysolr.Solr('http://localhost:8983/solr/articles/')

    def search(self, query, fields, weights=None):
        if weights is None:
            search_fields = fields
        else:
            if len(fields) != len(weights):
                raise ValueError('Fields & weights lengths should be equal!')
            search_fields = []
            for f, w in zip(fields, weights):
                search_fields.append(f + "^" + str(w))

        res = self.solr.search(q=query, **{
            'defType': 'edismax',
            'qf': 'title tags entities website type content_main',
            'q.op': 'OR'
        })

        return [w['id'] for w in res.docs]


def main():
    searcher = SolrSearcher()
    searcher.search("privacy", ["title", "tags", "entities", "website", "type", "content_main", "content_additional"])


if __name__ == '__main__':
    main()
