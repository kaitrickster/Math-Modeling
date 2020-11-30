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
    plt.close()


def export_best_schedule_to_csv(best_schedule):
    clusters = best_schedule.pairwise_hierarchical_clustering()
    row_list = []
    for i in range(len(clusters)):
        cluster = clusters[i]
        for student_id, faculty_id_list in cluster.items():
            temp = [student_id]
            for faculty_id in faculty_id_list:
                temp.append(faculty_id)
            row_list.append(temp)

        row_list.append(["-----"] * 5)

    df = pd.DataFrame(row_list, columns=["Student ID", "First Faculty ID", "Second Faculty ID",
                                         "Third Faculty ID", "Fourth Faculty ID"])
    df.to_csv(r"best_schedule.csv")


def plot_loss_history(optimizer):
    plt.plot(optimizer.loss_history)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.savefig("loss_curve.png")
    plt.close()
