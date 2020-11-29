from interview_group import *
from scipy import stats
from collections import defaultdict

PENALTY_FOR_IDENTICAL_GROUP = 50
PENALTY_FOR_OVERLAP = 10


class Schedule:
    def __init__(self, student_count, faculty_count):
        self.student_count = student_count
        self.faculty_count = faculty_count
        self.groups = []
        # self.student_dic = {}
        # self.faculty_dic = {}

    def init_schedule(self):
        for student_id in range(self.student_count):
            interview_group = InterviewGroup(student_id)
            interview_group.random_init(self.faculty_count)

            # self.update_student_dic(student_id, interview_group.student)
            # self.update_faculty_dic(interview_group.first_faculty.faculty_id, interview_group.first_faculty)
            # self.update_faculty_dic(interview_group.second_faculty.faculty_id, interview_group.second_faculty)
            # self.update_faculty_dic(interview_group.third_faculty.faculty_id, interview_group.third_faculty)
            # self.update_faculty_dic(interview_group.fourth_faculty.faculty_id, interview_group.fourth_faculty)

            self.groups.append(interview_group)

    def compute_cost(self):
        cost = 0
        faculty_interview_count_dict = {}
        faculty_student_map = defaultdict(set)
        for i in range(self.student_count):
            student_id = i
            group1 = self.groups[i]
            faculty_id_one, faculty_id_two, faculty_id_three, faculty_id_four = group1.faculty_id_list

            for faculty_id in group1.faculty_id_list:
                faculty_student_map[faculty_id].add(student_id)

            # first_faculty = group1.first_faculty
            # second_faculty = group1.second_faculty
            # third_faculty = group1.third_faculty
            # fourth_faculty = group1.fourth_faculty
            #
            # # possible overriding does not matter as length of student_id_list remains the same
            # faculty_interview_count_dict[first_faculty.faculty_id] = len(
            #     first_faculty.student_id_list)
            # faculty_interview_count_dict[second_faculty.faculty_id] = len(
            #     second_faculty.student_id_list)
            # faculty_interview_count_dict[third_faculty.faculty_id] = len(
            #     third_faculty.student_id_list)
            # faculty_interview_count_dict[fourth_faculty.faculty_id] = len(
            #     fourth_faculty.student_id_list)

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
        cost += (clipped_kl_divergence * 20)  # weight KL divergence by 20
        return cost

    # def update_student_dic(self, student_id, student):
    #     self.student_dic[student_id] = student
    #
    # def update_faculty_dic(self, faculty_id, faculty):
    #     self.faculty_dic[faculty_id] = faculty

    def perturb_faculty(self, student_id, faculty_id, which_faculty_idx):
        filter_set = set(self.groups[student_id].faculty_id_list)
        new_faculty_id = self.wrap_around(faculty_id, filter_set)
        self.groups[student_id].faculty_id_list[which_faculty_idx] = new_faculty_id

        # evict old faculty
        # old_faculty = self.faculty_dic[faculty_id]
        # # print(f"student_id = {student_id},  which_faculty = {which_faculty_idx}, faculty_id = {faculty_id}")
        # # print(f"student_id_list = {old_faculty.student_id_list}")
        # # old_faculty.student_id_list.remove(student_id)
        # self.update_faculty_dic(faculty_id, old_faculty)
        #
        # # update new faculty
        # if new_faculty_id in self.faculty_dic:
        #     new_faculty = self.faculty_dic[new_faculty_id]
        # else:
        #     new_faculty = Faculty(new_faculty_id)
        # new_faculty.add_interviewee_id(student_id)
        # self.update_faculty_dic(new_faculty_id, new_faculty)
        #
        # # update student
        # modified_student = self.student_dic[student_id]
        # modified_student.faculty_id_list = list(modified_student.faculty_id_list)
        # # modified_student.faculty_id_list.remove(faculty_id)
        # modified_student.faculty_id_list.append(new_faculty_id)
        # if which_faculty_idx == 0:
        #     modified_student.first = new_faculty
        # elif which_faculty_idx == 1:
        #     modified_student.second = new_faculty
        # elif which_faculty_idx == 2:
        #     modified_student.third = new_faculty
        # elif which_faculty_idx == 3:
        #     modified_student.fourth = new_faculty
        #
        # self.update_student_dic(student_id, modified_student)

    def cross_over_two_groups(self, student_id, faculty_id, which_faculty_idx):
        # group1, group2 = self.groups[group_idx1], self.groups[group_idx2]
        # faculty_id = group2.faculty_id_list[which_faculty_idx]
        return None

    def wrap_around(self, faculty_id, filter_set):
        new_faculty_id = faculty_id
        while new_faculty_id in filter_set:
            p = np.random.rand()
            if p >= 0.5:
                if faculty_id + 1 == self.faculty_count:
                    new_faculty_id = 0
                else:
                    new_faculty_id += 1
            else:
                if faculty_id - 1 < 0:
                    new_faculty_id = self.faculty_count - 1
                else:
                    new_faculty_id -= 1

        return new_faculty_id

    def __len__(self):
        return self.student_count

    def __getitem__(self, item):
        return self.groups[item]

    def __str__(self):
        return "\n".join([str(group) for group in self.groups])
