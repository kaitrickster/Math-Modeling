import argparse
from utils import *
from genetic_optimizer import GeneticOptimizer
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default="")
    parser.add_argument("--population_size", type=int, default="")
    parser.add_argument("--student_count", type=int, default="")
    parser.add_argument("--faculty_count", type=int, default="")
    parser.add_argument("--epoch", type=int, default="")
    parser.add_argument("--mutate_prob", type=float, default=0.3, required=False)
    parser.add_argument("--elite", type=int, default=10, required=False)
    parser.add_argument("--alpha", type=float, default=0.3, required=False)
    parser.add_argument("--beta", type=float, default=0.3, required=False)
    parser.add_argument("--hyperparam_search", type=bool, default=False, required=False)
    opt = parser.parse_args()
    np.random.seed(opt.seed)

    optimizer = GeneticOptimizer(population_size=opt.population_size, student_count=opt.student_count,
                                 faculty_count=opt.faculty_count, epoch=opt.epoch, mutate_prob=opt.mutate_prob,
                                 elite=opt.elite, alpha=opt.alpha, beta=opt.beta,
                                 hyperparam_search=opt.hyperparam_search)
    best_schedule = optimizer.evolution()

    plot_faculty_interview_bar(best_schedule.get_faculty_student_map())
    export_best_schedule_to_csv(best_schedule)
    plot_loss_history(optimizer)
