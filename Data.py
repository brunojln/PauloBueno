import csv
import numpy as np

class Data:
    @staticmethod
    def get_matrix_data(path):
        matrix = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                matrix.append([float(x) for x in row])
        return np.array(matrix)

    @staticmethod
    def get_vector_data(path):
        vector = []
        with open(path, 'r') as file:
            for line in file:
                vector.append(float(line.strip()))
        return np.array(vector)