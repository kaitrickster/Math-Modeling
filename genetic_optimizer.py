import copy
from schedule import *

MAX_ITER = 300


class GeneticOptimizer:
    def __init__(self, population_size, student_count, faculty_count, mutate_prob=0.3, elite=10):
        self.population_size = population_size
        self.student_count = student_count
        self.faculty_count = faculty_count
        self.mutate_prob = mutate_prob
        self.elite = elite
        self.population = []
        self.best_schedule = None
        self.lowest_cost = float("inf")

    def init_population(self):
        for i in range(self.population_size):
            schedule = Schedule(self.student_count, self.faculty_count)
            schedule.init_schedule()
            self.population.append(schedule)

    def filter_out_elite(self):
        cost_list = []
        for schedule in self.population:
            cost_list.append(schedule.compute_cost())
        idx_list = list(np.array(cost_list).argsort())
        return idx_list[:self.elite], cost_list[idx_list[0]]

    def mutate(self, elite_population):
        elite_idx = np.random.randint(0, self.elite - 1)
        elite_schedule_copy = copy.deepcopy(elite_population[elite_idx])

        for group in elite_schedule_copy:
            student_id = group.student_id
            which_faculty_idx = np.random.randint(0, COMMITTEE_SIZE - 1)
            faculty_id = group.faculty_id_list[which_faculty_idx]
            elite_schedule_copy.perturb_faculty(student_id, faculty_id, which_faculty_idx)

        return elite_schedule_copy

    def cross_over(self, elite_population):
        elite_idx_one = np.random.randint(0, self.elite - 1)
        elite_idx_two = np.random.randint(0, self.elite - 1)

        elite_schedule_copy = copy.deepcopy(elite_population[elite_idx_one])
        schedule_two = elite_population[elite_idx_two]
        elite_schedule_copy.cross_over_two_schedules(schedule_two)
        return elite_schedule_copy

    def evolution(self):
        self.init_population()

        for i in range(MAX_ITER):
            temp_elite_id_list, temp_lowest_cost = self.filter_out_elite()
            if temp_lowest_cost < self.lowest_cost:
                self.best_schedule = self.population[temp_elite_id_list[0]]
                self.lowest_cost = temp_lowest_cost

            print(f"lowest cost at iteration {i} : {self.lowest_cost}")
            fp = open("record.txt", "a")
            fp.write("lowest cost at iteration " + str(i) + " is : " + str(self.lowest_cost) + "\n")
            fp.close()

            new_population = [self.population[idx] for idx in temp_elite_id_list]

            while len(new_population) < self.population_size:
                if np.random.rand() <= self.mutate_prob:
                    new_schedule = self.mutate(new_population)
                else:
                    new_schedule = self.cross_over(new_population)
                new_population.append(new_schedule)

            self.population = new_population

        fp = open("record.txt", "a")
        fp.write(str(self.best_schedule))
        fp.close()
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
