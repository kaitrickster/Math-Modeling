import numpy as np
from student import *
from faculty import *

COMMITTEE_SIZE = 4


class InterviewGroup:
    def __init__(self, student_id):
        self.student = Student(student_id)
        self.student_id = student_id
        self.faculty_id_list = []
        # self.first_faculty = None
        # self.second_faculty = None
        # self.third_faculty = None
        # self.fourth_faculty = None
        self.faculties = []

    def random_init(self, faculty_count):
        faculty_id_list = np.random.choice(faculty_count, COMMITTEE_SIZE, replace=False)
        self.faculty_id_list = faculty_id_list

        first_faculty = Faculty(faculty_id_list[0])
        second_faculty = Faculty(faculty_id_list[1])
        third_faculty = Faculty(faculty_id_list[2])
        fourth_faculty = Faculty(faculty_id_list[3])

        self.student.assign_faculty_list(faculty_id_list)

        self.faculties = [first_faculty, second_faculty, third_faculty, fourth_faculty]

        # self.student.assign_faculties(self.faculties)

        # for faculty in self.faculties:
        #     faculty.add_student(self.student)

        # self.first_faculty = first_faculty
        # self.second_faculty = second_faculty
        # self.third_faculty = third_faculty
        # self.fourth_faculty = fourth_faculty

    def __str__(self):
        val = " ".join([str(faculty.faculty_id) for faculty in self.faculties])
        ret = f"{self.student.student_id} : {val}"
        return ret


# np.random.seed(0)
group = InterviewGroup(3)
group.random_init(10)
print(group)
