import random

# define the variables that can be tweaked
target = 'genetic algorithms'
populationSize = 1000               
mutationRate = 0.01

# DNA class defines the properties of an indivisual and the actions performed on them
class DNA:
    def __init__(self, length):
        self.fit = 0                                            # fitness value of the indivisual
        self.genes = []                                         # genes i.e. here it is a string of length target
        for i in range(length):
            self.genes.append(chr(random.randint(0, 150)))      # initialize the genes with random characters

    # find fitness of an indivisual wrt target
    def fitness(self, target):
        score = 0
        for i in range(len(target)):
            if self.genes[i] == target[i]:
                score += 1
        # normalize the values b/w 0-100 (%)
        self.fit = float(score) / len(target)
        
    # create new child from 2 parents
    def crossover(self, partner):
        child = DNA(0)
        midpoint = random.randint(0, len(self.genes)-1)
        child.genes[0:midpoint] = self.genes[0:midpoint]
        child.genes[midpoint:len(self.genes)] = partner.genes[midpoint:len(self.genes)]
        # for i in range(len(self.genes)):
        #     if i < midpoint:
        #         child.genes.append(self.genes[i])
        #     else:
        #         child.genes.append(partner.genes[i])
        return child
    
    # mutate the indivisual with defined mutation rate
    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if (random.random() < mutationRate):
                self.genes[i] = chr(random.randint(0, 150))
    
    # return the string value of the indivisual
    def getPhrase(self):
        return "".join(self.genes)

# Population class defines genetic algorithm methods and the required attributes
class Population:
    mutationRate = 0.0
    target = ""
    population = []
    matingPool = []
    finished = False
    perfectScore = 0        # 1 if the indivisual string matches the target string
    generation = 0

    def __init__(self, target, mutationRate, populationSize):
        self.target = target
        self.mutationRate = mutationRate
        for i in range(populationSize):
            self.population.append(DNA(len(target)))
        self.calcFitness()
        self.finished = False
        self.perfectScore = 1
    
    # calcualte fitness of all the indivisuals in the population
    def calcFitness(self):
        for indivisual in self.population:
            indivisual.fitness(self.target)
    
    # select indivisuals and add them to the mating pool based on roulette wheel probability method
    def selection(self):
        self.matingPool.clear()
        for indivisual in self.population:
            n = int(indivisual.fit * 100)
            for i in range(n):
                self.matingPool.append(indivisual)

    # generate new child by randomly selecting two parents from the mating pool, mutate it, and then add it to the next geneartion
    def generate(self):
        for i in range(len(self.population)):
            parents = random.choices(self.matingPool, k=2)
            child = parents[0].crossover(parents[1])
            child.mutate(self.mutationRate)
            self.population[i] = child
        self.generation += 1
    
    # get te top performing indivisual in the generation
    def getBest(self):
        worldRecord = 0
        index = 0
        for i in range(len(self.population)):
            if self.population[i].fit > worldRecord:
                worldRecord = self.population[i].fit
                index = i
        if worldRecord == self.perfectScore:
            self.finished = True
        return self.population[index].getPhrase()


if __name__ == "__main__":
    # seed random function
    random.seed(1)

    # generate population
    population = Population(target, mutationRate, populationSize)

    while(True):
        population.selection()
        population.generate()
        population.calcFitness()
        print('"' + str(population.getBest()) + '"' +
            ' in generation :' + str(population.generation))
        if population.finished:
            break