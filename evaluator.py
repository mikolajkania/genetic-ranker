import csv
from searcher import Searcher


class Evaluator:
    searcher = Searcher()
    query_to_id = {}
    fields = ["title", "tags", "entities", "website", "type", "content_main", "content_additional"]

    def __init__(self):
        with open('queries.csv') as csvfile:
            model_reader = csv.reader(csvfile, delimiter=',')
            for row in model_reader:
                self.query_to_id[row[0]] = row[1]

    def quality(self):
        valid = 0

        for key, value in self.query_to_id.items():
            first = self.searcher.search(key, self.fields)
            if first == value:
                print('Valid result for query=' + key)
                valid += 1
            else:
                print('Invalid result for query=' + key + ', expected doc with id=' + value)
            print()

        quality = valid / len(self.query_to_id)
        print('Search quality is=' + str(quality))

        return quality


def main():
    evaluator = Evaluator()
    evaluator.quality()


if __name__ == '__main__':
    main()
