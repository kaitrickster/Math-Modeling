import numpy as np

COMMITTEE_SIZE = 4


class InterviewGroup:
    def __init__(self, student_id):
        self.student_id = student_id
        self.faculty_id_list = []

    def random_init(self, faculty_count):
        """
        randomly initialize faculty group by sampling without replacement

        Args:
            faculty_count: number of faculties to interview a single student
        """
        faculty_id_list = np.random.choice(faculty_count, COMMITTEE_SIZE, replace=False)
        self.faculty_id_list = faculty_id_list

    def __str__(self):
        val = " ".join([str(faculty_id) for faculty_id in self.faculty_id_list])
        ret = f"{self.student_id} : {val}"
        return ret
