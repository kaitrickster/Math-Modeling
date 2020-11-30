import argparse

from genetic_optimizer import GeneticOptimizer
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default='')
    parser.add_argument('--population_size', type=int, default='')
    parser.add_argument('--student_count', type=int, default='')
    parser.add_argument('--faculty_count', type=int, default='')
    opt = parser.parse_args()
    np.random.seed(opt.seed)

    optimizer = GeneticOptimizer(population_size=opt.population_size, student_count=opt.student_count,
                                 faculty_count=opt.faculty_count)
    optimizer.evolution()
    fp = open("record.txt", "a")
    fp.write("\n" + str(optimizer.best_schedule.get_faculty_student_map()))
    fp.close()
