import numpy as np
from scipy import stats
from interview_group import *

PENALTY_FOR_IDENTICAL_GROUP = 100
PENALTY_FOR_OVERLAP = 10

#
# def filter_out_elite(population, elite, faculty_count):
#     cost_list = []
#     n = len(population[0])
#
#     for schedule in population:
#         cost = 0
#         faculty_interview_count_dict = {}
#         for i in range(n):
#             cur_group_first_faculty = schedule[i].first_faculty
#             cur_group_second_faculty = schedule[i].second_faculty
#             cur_group_third_faculty = schedule[i].third_faculty
#             cur_group_fourth_faculty = schedule[i].fourth_faculty
#             # possible overriding does not matter as length of student_id_list remains the same
#             faculty_interview_count_dict[cur_group_first_faculty.faculty_id] = len(
#                 cur_group_first_faculty.student_id_list)
#             faculty_interview_count_dict[cur_group_second_faculty.faculty_id] = len(
#                 cur_group_second_faculty.student_id_list)
#             faculty_interview_count_dict[cur_group_third_faculty.faculty_id] = len(
#                 cur_group_third_faculty.student_id_list)
#             faculty_interview_count_dict[cur_group_fourth_faculty.faculty_id] = len(
#                 cur_group_fourth_faculty.student_id_list)
#
#             for j in range(i):
#                 first_faculty_list = schedule[j].faculty_id_list
#                 second_faculty_list = schedule[j].faculty_id_list
#                 first_faculty_group = set(first_faculty_list)
#                 second_faculty_group = set(second_faculty_list)
#
#                 overlap = first_faculty_group.intersection(second_faculty_group)
#                 if len(overlap) == 4:  # two groups have 4 identical faculty
#                     cost += PENALTY_FOR_IDENTICAL_GROUP
#                 elif len(overlap) >= 2:
#                     # if any two or three in the first_faculty group are present in the second_faculty group
#                     cost += PENALTY_FOR_OVERLAP
#
#         # calculate metric that measures if each faculty interviews similar amount of students
#         # scipy normalize two lists before computing KL divergence
#         vals = [faculty_interview_count_dict[faculty_id] if faculty_id in faculty_interview_count_dict else 0 for
#                 faculty_id in range(faculty_count)]
#         avg = sum(vals) / len(vals)
#         target_distribution = [avg for _ in range(len(vals))]
#         clipped_kl_divergence = np.clip(stats.entropy(vals, target_distribution), 0, 1)
#         cost += (clipped_kl_divergence * 10)  # weight KL divergence by 10
#
#         cost_list.append(cost)
#
#     idx_list = list(np.array(cost_list).argsort())
#     return idx_list[:elite], cost_list[idx_list[0]]


def to_string(calendar):
    ret = []
    for group in calendar:
        ret.append(str(group))
    return "\n".join(ret)
