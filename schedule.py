from interview_group import *
from scipy import stats
from collections import defaultdict

PENALTY_FOR_IDENTICAL_GROUP = 10
PENALTY_FOR_OVERLAP = 1


class Schedule:
    def __init__(self, student_count, faculty_count):
        self.student_count = student_count
        self.faculty_count = faculty_count
        self.groups = []

    def init_schedule(self):
        for student_id in range(self.student_count):
            interview_group = InterviewGroup(student_id)
            interview_group.random_init(self.faculty_count)
            self.groups.append(interview_group)

    def compute_cost(self):
        cost = 0
        faculty_student_map = defaultdict(set)
        for i in range(self.student_count):
            student_id = i
            group1 = self.groups[i]

            for faculty_id in group1.faculty_id_list:
                faculty_student_map[faculty_id].add(student_id)

            for j in range(i):
                group2 = self.groups[j]
                first_faculty_list = group1.faculty_id_list
                second_faculty_list = group2.faculty_id_list
                first_faculty_group = set(first_faculty_list)
                second_faculty_group = set(second_faculty_list)

                overlap = first_faculty_group.intersection(second_faculty_group)
                if len(overlap) == COMMITTEE_SIZE:
                    cost += PENALTY_FOR_IDENTICAL_GROUP
                elif len(overlap) >= 2:
                    cost += PENALTY_FOR_OVERLAP

        # calculate metric that measures if each faculty interviews similar amount of students
        # scipy normalize a list to probability distribution before computing KL divergence
        vals = [len(faculty_student_map[faculty_id]) if faculty_id in faculty_student_map else 0 \
                for faculty_id in range(self.faculty_count)]
        avg = sum(vals) / len(vals)
        target_distribution = [avg for _ in range(len(vals))]
        clipped_kl_divergence = np.clip(stats.entropy(vals, target_distribution), 0, 1)
        cost += clipped_kl_divergence
        return cost

    def perturb_faculty(self, student_id, faculty_id, which_faculty_idx):
        filter_set = set(self.groups[student_id].faculty_id_list)
        new_faculty_id = self.wrap_around(faculty_id, filter_set)
        self.groups[student_id].faculty_id_list[which_faculty_idx] = new_faculty_id

    def cross_over_two_schedules(self, other):
        for group1, group2 in zip(self.groups, other.groups):
            which_faculty_idx = np.random.randint(0, COMMITTEE_SIZE - 1)
            candidate = group2.faculty_id_list[which_faculty_idx]
            filter_set = set(group1.faculty_id_list)
            if candidate in filter_set:
                candidate = self.wrap_around(candidate, filter_set)

            group1.faculty_id_list[which_faculty_idx] = candidate

    def wrap_around(self, faculty_id, filter_set):
        new_faculty_id = faculty_id
        while new_faculty_id in filter_set:
            p = np.random.rand()
            if p >= 0.5:
                new_faculty_id += 1
                if new_faculty_id >= self.faculty_count:
                    new_faculty_id = 0
            else:
                new_faculty_id -= 1
                if new_faculty_id < 0:
                    new_faculty_id = self.faculty_count - 1

        return new_faculty_id

    def __len__(self):
        return self.student_count

    def __getitem__(self, item):
        return self.groups[item]

    def __str__(self):
        return "\n".join([str(group) for group in self.groups])
