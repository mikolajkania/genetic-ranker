from deap import creator, base, tools, algorithms
import random

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register(
    "random_char",
    random.choice,
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

DIM = 2  # matrix side

toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.random_char,
    n=DIM * DIM)


# nadpisanie toString dla individuala
def __str__(individual):
    s = ""
    for i in range(len(individual)):
        s += individual[i]
    if i % DIM == DIM - 1:
        s += '#'
    return s


creator.Individual.__str__ = __str__

print(toolbox.individual())

toolbox.register("population",
                 tools.initRepeat,
                 list,
                 toolbox.individual,
                 n=2)

print(toolbox.population())
