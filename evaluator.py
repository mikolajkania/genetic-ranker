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
                self.query_to_positions[row[0]] = Evaluator.Results(id=results[0], expected=results[1][3:], adequate=results[2][3:])

    def quality(self, weights=None, verbose=None):
        valid = 0

        for key, value in self.query_to_positions.items():
            first = self.searcher.search(key, self.fields, weights)
            if first == value:
                valid += 1
            elif verbose:
                print('Invalid result for query=' + key + ', expected doc with id=' + value)

        quality = valid / len(self.query_to_positions) * 100

        if verbose:
            print("Search quality is [%(q)d%%] for %(w)s:" % {'q': quality, 'w': weights})

        return quality

    class Results:
        id = -1
        expected_in_top = -1
        adequate_in_top = -1

        def __init__(self, id, expected, adequate):
            self.id = id
            self.expected_in_top = expected
            self.adequate_in_top = adequate

        def __str__(self):
            return "id: " + self.id + ", expected in top: " + self.expected_in_top + ", adequate in top: " + self.adequate_in_top

        def __repr__(self):
            return self.__str__()


def main():
    evaluator = Evaluator()
    evaluator.quality([5, 3, 1, 2, 2, 1, 0.5])


if __name__ == '__main__':
    main()
