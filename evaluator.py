import csv
from searcher import Searcher


class Evaluator:
    searcher = Searcher()
    query_to_positions = {}
    fields = ["title", "tags", "entities", "website", "type", "content_main", "content_additional"]

    def __init__(self):
        with open('queries.csv') as csvfile:
            model_reader = csv.reader(csvfile, delimiter=',')
            for row in model_reader:
                results = row[1].split(sep=":")
                self.query_to_positions[row[0]] = Evaluator.Expected(docId=results[0], expected=results[1][3:], adequate=results[2][3:])

    def quality(self, weights=None, verbose=None):
        score = 0

        for key, value in self.query_to_positions.items():
            results_ids = self.searcher.search(key, self.fields, weights)

            if len(results_ids) == 0:
                continue

            if value.docId in results_ids[:value.expected_in_top]:
                score += 1
            elif value.docId in results_ids[:value.adequate_in_top]:
                score += 0.5
            else:
                continue

        quality = round(score / len(self.query_to_positions) * 100, 1)

        if verbose:
            print("Search quality is [%(q)d%%] for %(w)s:" % {'q': quality, 'w': weights})

        return quality

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
