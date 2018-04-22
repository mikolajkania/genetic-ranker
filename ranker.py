import random
from deap import creator, base, tools, algorithms
from math import pow
from math import copysign
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
        self.toolbox.register("mut_slightly", self.mut_slightly)
        self.toolbox.register("mutate", self.toolbox.mut_slightly, low=0, up=10)
        # individuals of the current gen are replaced by the 'fittest'
        self.toolbox.register("select", tools.selTournament, tournsize=2)

    # weights must be a tuple so that multi-objective and single objective fitnesses can be treated the same way
    def fitness(self, individual):
        fitness = self.evaluator.quality(individual)
        # print('For individual=' + str(individual) + ', fitness is=' + str(fitness))
        return fitness,

        # z = pow(individual[0], 2) - pow(individual[1], 2),
        # # print(str(individual) + ' ' + str(z[0]))
        # return z

    # update individuals's fitness
    def evaluate_population_fitnesses(self, pop):
        pop_fit = self.toolbox.map(self.toolbox.evaluate, pop)
        for individual, fitness in zip(pop, pop_fit):
            individual.fitness.values = fitness

    def mut_slightly(self, individual, low, up):
        size = len(individual)
        original = individual[:]
        gene = random.randint(0, size-1)
        individual[gene] = random.randint(low, up)

        if original != individual:
            print('muted: ' + str(original) + '(' + str(self.fitness(original)[0]) + ') => ' +
                  str(individual) + '(' + str(self.fitness(individual)[0]) + ')')
        return individual,


def main():
    ranker = Ranker()
    hof = tools.HallOfFame(1)

    MU, LAMBDA = 10, 20

    # create an initial population of individuals (where each individual is a list of integers)
    population = ranker.toolbox.population(n=MU)
    # print(population)

    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    population, logbook = algorithms.eaMuPlusLambda(population, ranker.toolbox, mu=MU, lambda_=LAMBDA, cxpb=0.6,
                                                    mutpb=0.2, ngen=10, halloffame=hof)
    # print(population)
    print_best(population, ranker, hof)

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

    dbg = 1


def print_best(population, ranker, hof):
    top = tools.selBest(population, k=1)
    print('\n')
    print('best of last population: ' + str(top[0]) + ' ' + str(ranker.fitness(top[0])))
    print('best overall: ' + str(hof[0]) + ' ' + str(ranker.fitness(hof[0])))


if __name__ == "__main__":
    main()
