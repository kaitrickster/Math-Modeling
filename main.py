from genetic_optimizer import *

if __name__ == "__main__":
    optimizer = GeneticOptimizer(100, 379, 24)
    optimizer.evolution()
    print(str(optimizer.best_schedule))

