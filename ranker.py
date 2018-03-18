import random
from deap import creator, base, tools, algorithms
from math import log1p
from math import sin


class Ranker:
    # all objects will be stored in DEAP container called Toolbox
    toolbox = base.Toolbox()

    def __init__(self):
        # creator - factory to create new classes with given attributes
        # we will be maximizing a single objective fitness
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # an attribute ('gene')
        self.toolbox.register("attr_int", random.randint, -10, 10)
        # individual consisting of elements ('genes')
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_int, n=2)
        # list of individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        # fitness function
        self.toolbox.register("evaluate_fun", self.fitness)
        # crossover operator
        self.toolbox.register("mate", tools.cxTwoPoint)
        # a mutation operator
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        # individuals of the current gen are replaced by the 'fittest' of x individuals from the current gen
        self.toolbox.register("select", tools.selTournament, tournsize=2)

    # weights must be a tuple so that multi-objective and single objective fitnesses can be treated the same way
    def fitness(self, individual):
        x = individual[0]
        y = individual[1]
        if y == 0 or x < 0:
            return -5,
        return sin(x/y)-log1p(x),

    # update individuals's fitness
    def evaluate_population_fitnesses(self, pop):
        pop_fit = self.toolbox.map(self.toolbox.evaluate_fun, pop)
        for individual, fitness in zip(pop, pop_fit):
            individual.fitness.values = fitness


def main():
    ranker = Ranker()

    # create an initial population of individuals (where each individual is a list of integers)
    population = ranker.toolbox.population(n=4)

    for gen in range(100):
        # CXPB  is the probability with which two individuals are crossed
        # MUTPB is the probability for mutating an individual
        offspring = algorithms.varAnd(population, ranker.toolbox, cxpb=0.5, mutpb=0.1)
        ranker.evaluate_population_fitnesses(offspring)
        population = ranker.toolbox.select(offspring, k=len(population))
        print(population)
        top = tools.selBest(population, k=1)
        print(top)
        print(ranker.fitness(top[0]))
        print('\n')

    # fits = [ind.fitness.values[0] for ind in population]
    # length = len(population)
    # mean = sum(fits) / length
    # sum2 = sum(x * x for x in fits)
    # std = abs(sum2 / length - mean ** 2) ** 0.5
    #
    # print("  Min %s" % min(fits))
    # print("  Max %s" % max(fits))
    # print("  Avg %s" % mean)
    # print("  Std %s" % std)




if __name__ == "__main__":
    main()
