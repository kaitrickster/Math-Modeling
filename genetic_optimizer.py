import copy
from schedule import *


class GeneticOptimizer:
    def __init__(self, population_size, student_count, faculty_count, epoch, mutate_prob=0.56,
                 elite=16, alpha=0.45, beta=0.02, hyperparam_search=False):
        self.population_size = population_size
        self.student_count = student_count
        self.faculty_count = faculty_count
        self.mutate_prob = mutate_prob
        self.elite = elite
        self.epoch = epoch
        self.alpha = alpha
        self.beta = beta
        self.hyperparam_search = hyperparam_search
        self.population = []
        self.best_schedule = None
        self.lowest_loss = float("inf")
        self.loss_history = []

    def init_population(self):
        for i in range(self.population_size):
            schedule = Schedule(self.student_count, self.faculty_count)
            schedule.init_schedule()
            self.population.append(schedule)

    def filter_out_elite(self):
        loss_list = []
        for schedule in self.population:
            loss_list.append(schedule.compute_loss())
        idx_list = list(np.array(loss_list).argsort())
        return idx_list[:self.elite], loss_list[idx_list[0]]

    def mutate(self, elite_population):
        elite_idx = np.random.randint(0, self.elite - 1)
        elite_schedule_copy = copy.deepcopy(elite_population[elite_idx])

        for group in elite_schedule_copy:
            student_id = group.student_id
            which_faculty_idx = np.random.randint(0, COMMITTEE_SIZE - 1)
            faculty_id = group.faculty_id_list[which_faculty_idx]
            if np.random.rand() <= self.alpha:
                elite_schedule_copy.perturb_faculty(student_id, faculty_id, which_faculty_idx)

        return elite_schedule_copy

    def cross_over(self, elite_population):
        elite_idx_one = np.random.randint(0, self.elite - 1)
        elite_idx_two = np.random.randint(0, self.elite - 1)

        elite_schedule_copy = copy.deepcopy(elite_population[elite_idx_one])
        schedule_two = elite_population[elite_idx_two]
        elite_schedule_copy.cross_over_two_schedules(schedule_two, self.beta)
        return elite_schedule_copy

    def evolution(self):
        self.init_population()

        for i in range(self.epoch):
            temp_elite_id_list, temp_lowest_cost = self.filter_out_elite()
            self.loss_history.append(temp_lowest_cost)
            if temp_lowest_cost < self.lowest_loss:
                self.best_schedule = self.population[temp_elite_id_list[0]]
                self.lowest_loss = temp_lowest_cost

            if not self.hyperparam_search:
                print(f"lowest cost at iteration {i} : {self.lowest_loss}")
            fp = open("record.txt", "a")
            if i == self.epoch - 1:
                fp.write(str(self.lowest_loss) + "\n")
            else:
                fp.write(str(self.lowest_loss) + ",")
            fp.close()

            new_population = [self.population[idx] for idx in temp_elite_id_list]

            while len(new_population) < self.population_size:
                if np.random.rand() <= self.mutate_prob:
                    new_schedule = self.mutate(new_population)
                else:
                    new_schedule = self.cross_over(new_population)
                new_population.append(new_schedule)

            self.population = new_population

        if self.hyperparam_search:
            print(f"current setting : mutate_prob = {self.mutate_prob}, elite = {self.elite}, alpha = {self.alpha}, "
                  f"beta = {self.beta}.  \n         Lowest loss = {self.lowest_loss} \n")

        return self.best_schedule

    def __str__(self):
        ret = []
        for calendar in self.population:
            for interview_group in calendar:
                ret.append(str(interview_group))
            ret.append("")
        return "\n".join(ret)

    def __getitem__(self, item):
        return self.population[item]
