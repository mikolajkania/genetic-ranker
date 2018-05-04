import random

from deap import creator, base, tools, algorithms

from evaluator import Evaluator


class Ranker:
    # all objects will be stored in DEAP container called Toolbox
    toolbox = base.Toolbox()
    evaluator = Evaluator()

    def __init__(self):
        # creator - factory to create new classes with given attributes
        # we will be maximizing a single objective fitness
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # an attribute ('gene')
        self.toolbox.register("attr_int", random.randint, 0, 10)
        # individual consisting of elements ('genes')
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_int, n=7)
        # list of individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        # fitness function
        self.toolbox.register("evaluate", self.fitness)
        # crossover operator
        self.toolbox.register("mate", tools.cxTwoPoint)
        # a mutation operator
        self.toolbox.register("mutate_slightly", self.mutate_random_resetting)
        self.toolbox.register("mutate", self.toolbox.mutate_slightly, low=0, up=10, verbose=True)
        # individuals of the current gen are replaced by the 'fittest'
        self.toolbox.register("select", tools.selTournament, tournsize=2)

    # weights must be a tuple so that multi-objective and single objective fitnesses can be treated the same way
    def fitness(self, individual):
        fitness = self.evaluator.quality(individual)
        # print('For individual=' + str(individual) + ', fitness is=' + str(fitness))
        return fitness,

    # update individuals's fitness
    def evaluate_population_fitnesses(self, pop):
        pop_fit = self.toolbox.map(self.toolbox.evaluate, pop)
        for individual, fitness in zip(pop, pop_fit):
            individual.fitness.values = fitness

    def mutate_random_resetting(self, individual, low, up, verbose=None):
        size = len(individual)
        original = individual[:]
        gene = random.randint(0, size - 1)
        individual[gene] = random.randint(low, up)

        if verbose:
            self.print_different(original, individual)

        return individual,

    def print_different(self, original, individual):
        # todo how many
        if original != individual:
            original_fitness = self.fitness(original)[0]
            individual_fitness = self.fitness(individual)[0]

            diff = individual_fitness - original_fitness
            if diff > 0:
                message = '[' + self.contant_length('+' + str(diff)) + ']'
            elif diff < 0:
                message = '[' + self.contant_length(str(diff)) + ']'
            else:
                message = '[' + self.contant_length('') + ']'

            message = message + ' muted: ' + str(original) + '(' + str(original_fitness) + ') => ' + \
                      str(individual) + '(' + str(individual_fitness) + ')'

            print(message)

    def contant_length(self, text):
        return text.ljust(5)


def main():
    ranker = Ranker()
    hof = tools.HallOfFame(5)

    MU, LAMBDA = 20, 40

    # create an initial population of individuals (where each individual is a list of integers)
    population = ranker.toolbox.population(n=MU)
    # print(population)

    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    population, logbook = algorithms.eaMuPlusLambda(population, ranker.toolbox, mu=MU, lambda_=LAMBDA, cxpb=0.6,
                                                    mutpb=0.2, ngen=5, halloffame=hof)
    # print(population)
    print_best(population, ranker, hof)


def print_best(population, ranker, hof):
    top = tools.selBest(population, k=1)
    print('\n')
    print('best of last population: {0} {1}%%'.format(str(top[0]), str(ranker.fitness(top[0])[0])))
    print('best overall: {0} {1}%%'.format(str(hof[0]), str(ranker.fitness(hof[0])[0])))
    print('hall of fame: {0}'.format(str(hof)))


if __name__ == "__main__":
    main()
