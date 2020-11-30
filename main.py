from genetic_optimizer import GeneticOptimizer
import numpy as np

if __name__ == "__main__":
    np.random.seed(2020)
    optimizer = GeneticOptimizer(population_size=100, student_count=20, faculty_count=20)
    optimizer.evolution()
    print(optimizer.best_schedule.get_faculty_student_map())
