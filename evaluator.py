import configparser
import csv
from essearcher import ESSearcher
from solrsearcher import SolrSearcher


class Evaluator:
    query_to_positions = {}
    fields = ["title", "tags", "entities", "website", "type", "content_main", "content_additional"]
    weights_to_score = {}
    searcher = None
    statistics = None

    def __init__(self):
        with open('queries.csv', encoding='utf-8') as csvfile:
            model_reader = csv.reader(csvfile, delimiter=',')
            for row in model_reader:
                results = row[1].split(sep=":")
                self.query_to_positions[row[0]] = Evaluator.Expected(docId=results[0],
                                                                     expected=results[1][3:],
                                                                     adequate=results[2][3:])
        self.statistics = Evaluator.Statistics()
        config = configparser.ConfigParser()
        config.read('properties.ini')
        searcher = config['DEFAULT']['searcher']
        if searcher == 'ES':
            self.searcher = ESSearcher()
        elif searcher == 'Solr':
            self.searcher = SolrSearcher()
        else:
            raise ValueError('Illegal searcher value')

    def quality(self, weights=None, verbose=None):
        self.statistics.total += 1

        cache_key = self.key(weights)
        if cache_key in self.weights_to_score:
            self.statistics.cached_values += 1
            return self.weights_to_score[cache_key]
        else:
            self.statistics.cache_retrievals += 1

        score = 0

        for key, value in self.query_to_positions.items():
            results_ids = self.searcher.search(key, self.fields, weights)

            if len(results_ids) == 0:
                continue

            # todo check whether types are equal
            if value.docId in results_ids[:value.expected_in_top]:
                score += 1
            elif value.docId in results_ids[:value.adequate_in_top]:
                score += 0.5
            else:
                continue

        quality = round(score / len(self.query_to_positions) * 100, 1)

        if verbose:
            print("Search quality is [%(q)d%%] for %(w)s:" % {'q': quality, 'w': weights})

        self.weights_to_score[cache_key] = quality

        return quality

    @staticmethod
    def key(weights):
        return tuple(weights)

    def getCacheLength(self):
        return len(self.weights_to_score)

    class Statistics:
        total = 0
        cache_retrievals = 0
        cached_values = 0

        def __str__(self) -> str:
            return "Total evaluations: " + str(self.total) + ", " + \
                   "cached values: " + str(self.cached_values) + \
                   ", retrivals from cache: " + str(self.cache_retrievals) + "."

    class Expected:
        docId = -1
        expected_in_top = -1
        adequate_in_top = -1

        def __init__(self, docId, expected, adequate):
            self.docId = docId
            self.expected_in_top = int(expected)
            self.adequate_in_top = int(adequate)

        def __str__(self):
            return "id: " + self.docId + ", expected in top: " + str(self.expected_in_top) + \
                   ", adequate in top: " + str(self.adequate_in_top)

        def __repr__(self):
            return self.__str__()


def main():
    evaluator = Evaluator()
    evaluator.quality([5, 3, 1, 2, 2, 1, 0.5])


if __name__ == '__main__':
    main()
