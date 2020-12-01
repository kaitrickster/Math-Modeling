from interview_group import *
from scipy import stats
from collections import defaultdict

PENALTY_FOR_IDENTICAL_GROUP = 1000000
PENALTY_FOR_OVERLAP = 1
PENALTY_WEIGHT_FOR_PAIRWISE_OVERLAP = 0.01


class Schedule:
    def __init__(self, student_count, faculty_count):
        self.student_count = student_count
        self.faculty_count = faculty_count
        self.groups = []
        self.clusters = []

    def init_schedule(self):
        """
        for each student in the schedule, randomly initialize the faculty committee
        """
        for student_id in range(self.student_count):
            interview_group = InterviewGroup(student_id)
            interview_group.random_init(self.faculty_count)
            self.groups.append(interview_group)

    def compute_loss(self):
        """
        compute loss for current schedule subject to the following requirements
            R1. Each faculty member interviews similar amount of students;
            R2. Two interview groups cannot have 4 identical interviewing faculty;
            R3. Two interview groups having 2-3 identical interviewing faculty should be avoided;
            R4. The number of students being interviewed by any pair of faculty members should be as small as possible.

        Returns:
            the loss value
        """
        loss = 0
        faculty_student_map = defaultdict(set)
        for i in range(1, self.student_count):
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
                    # penalty for R2: Two interview groups cannot have 4 identical interviewing faculty;
                    loss += PENALTY_FOR_IDENTICAL_GROUP
                elif len(overlap) >= 2:
                    # penalty for R3: Two interview groups having 2-3 identical interviewing faculty should be avoided;
                    loss += PENALTY_FOR_OVERLAP

        # calculate metric that measures R1: Each faculty member interviews similar amount of students
        # scipy normalize a list to a probability distribution before computing KL divergence
        vals = [len(faculty_student_map[faculty_id]) if faculty_id in faculty_student_map else 0
                for faculty_id in range(self.faculty_count)]
        avg = sum(vals) / len(vals)
        target_distribution = [avg for _ in range(len(vals))]
        clipped_kl_divergence = np.clip(stats.entropy(vals, target_distribution), 0, 1)
        loss += (clipped_kl_divergence * 10)

        # calculate loss for R4:
        #   The number of students being interviewed by any pair of faculty members should be as small as possible.
        for i in range(1, self.faculty_count):
            for j in range(i):
                student_group_one = set(faculty_student_map[i])
                student_group_two = set(faculty_student_map[j])
                overlap_count = len(student_group_one.intersection(student_group_two))
                loss += (overlap_count * PENALTY_WEIGHT_FOR_PAIRWISE_OVERLAP)

        return loss

    def perturb_faculty(self, student_id, faculty_id, which_faculty_idx):
        """
        given the student_id, perturb its faculty group

        Args:
            student_id: the chosen student
            faculty_id: which faculty to perturb
            which_faculty_idx: the index of faculty in the student's faculty_id_list
        """
        filter_set = set(self.groups[student_id].faculty_id_list)
        new_faculty_id = self.wrap_around(faculty_id, filter_set)
        self.groups[student_id].faculty_id_list[which_faculty_idx] = new_faculty_id

    def cross_over_two_schedules(self, other, beta):
        for group1, group2 in zip(self.groups, other.groups):
            which_faculty_idx = np.random.randint(0, COMMITTEE_SIZE - 1)
            candidate = group2.faculty_id_list[which_faculty_idx]
            filter_set = set(group1.faculty_id_list)
            if candidate in filter_set:
                candidate = self.wrap_around(candidate, filter_set)

            if np.random.rand() <= beta:
                group1.faculty_id_list[which_faculty_idx] = candidate

    def wrap_around(self, faculty_id, filter_set):
        """
        wrap around the target faculty_id while ensuring that it does not overlap with the filter_set

        Args:
            faculty_id: the faculty that we want to change

        Returns:
            the new faculty_id
        """
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

    def get_faculty_student_map(self):
        """
        construct map {faculty_id : list of student ids that the faculty interview}

        Returns:
            dictionary: {faculty_id : list of student ids that the faculty interview}
        """
        faculty_student_map = defaultdict(set)
        for student_id in range(self.student_count):
            group1 = self.groups[student_id]
            for faculty_id in group1.faculty_id_list:
                faculty_student_map[faculty_id].add(student_id)

        return faculty_student_map

    def hierarchical_clustering(self):
        """
        perform bottom up hierarchical clustering by merging two clusters

        Returns
           list of final clusters
        """
        i = 1
        while i < len(self.groups):
            cur_faculty_group = set(self.groups[i].faculty_id_list)
            prev_faculty_group = set(self.groups[i - 1].faculty_id_list)
            if len(cur_faculty_group.intersection(prev_faculty_group)) == 0:
                cluster = {self.groups[i - 1].student_id: self.groups[i - 1].faculty_id_list,
                           self.groups[i].student_id: self.groups[i].faculty_id_list}
                self.clusters.append(cluster)
            else:
                self.clusters.append({self.groups[i - 1].student_id: self.groups[i - 1].faculty_id_list})
                self.clusters.append({self.groups[i].student_id: self.groups[i].faculty_id_list})

            if i + 2 == len(self.groups):
                self.clusters.append({self.groups[i + 1].student_id: self.groups[i + 1].faculty_id_list})
            i += 2

        count = len(self.clusters) * 3
        for _ in range(count):
            idx1 = np.random.randint(0, len(self.clusters) - 1)
            idx2 = np.random.randint(0, len(self.clusters) - 1)
            if idx1 == idx2:
                continue
            self.merge_two_cluster(idx1, idx2)

        return self.clusters

    def merge_two_cluster(self, i, j):
        """
        merge two interview clusters if their faculty groups do not overlap

        Args
            i: index of first cluster
            j: index of second cluster
        """
        one, two = self.clusters[i], self.clusters[j]
        group_one_list, group_two_list = [], []
        for key, val in one.items():
            group_one_list.extend(val)
        for key, val in two.items():
            group_two_list.extend(val)
        group_one = set(group_one_list)
        group_two = set(group_two_list)
        if len(group_one.intersection(group_two)) == 0:
            for student_id, faculty_id_list in two.items():
                self.clusters[i][student_id] = faculty_id_list
            self.clusters.pop(j)

    def __len__(self):
        return self.student_count

    def __getitem__(self, item):
        return self.groups[item]

    def __str__(self):
        return "\n".join([str(group) for group in self.groups])
