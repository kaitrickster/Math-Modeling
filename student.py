class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.faculty_id_list = []
        # self.faculties = []

    def assign_faculty_list(self, faculty_id_list):
        self.faculty_id_list = faculty_id_list

    # def assign_faculties(self, faculties):
    #     self.faculties = faculties

    # def __str__(self):
    #     ret = str(self.student_id) + " : "
    #     for faculty in self.faculties:
    #         ret += str(faculty.faculty_id) + " "
    #     return ret