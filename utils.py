import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_faculty_interview_bar(faculty_student_map):
    vals = [len(value) for value in list(faculty_student_map.values())]
    x = np.arange(len(vals))
    plt.bar(x, height=vals)
    plt.title("Number of Students Each Faculty Interview")
    plt.xlabel("faculty_id")
    plt.ylabel("Student Count")
    plt.savefig('faculty_student_count.png')


def plot_best_schedule(best_schedule):
    mat = [group.faculty_id_list for group in best_schedule]
    rows = ["student id : " + str(student_id) for student_id in range(len(mat))]
    columns = ["First Faculty ID", "Second Faculty ID", "Third Faculty ID", "Fourth Faculty ID"]
    df = pd.DataFrame(mat, columns=columns)
    df.index = rows
    df.to_csv(r"data.csv")

