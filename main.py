import argparse
from utils import *
from genetic_optimizer import GeneticOptimizer
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default='')
    parser.add_argument('--population_size', type=int, default='')
    parser.add_argument('--student_count', type=int, default='')
    parser.add_argument('--faculty_count', type=int, default='')
    parser.add_argument('--epoch', type=int, default='')
    opt = parser.parse_args()
    np.random.seed(opt.seed)

    optimizer = GeneticOptimizer(population_size=opt.population_size, student_count=opt.student_count,
                                 faculty_count=opt.faculty_count, epoch=opt.epoch)
    best_schedule = optimizer.evolution()

    plot_faculty_interview_bar(best_schedule.get_faculty_student_map())
    plot_best_schedule(best_schedule)
