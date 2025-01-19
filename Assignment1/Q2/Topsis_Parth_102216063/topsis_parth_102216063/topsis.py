import numpy as np

class Topsis:

    @staticmethod
    def topsis(matrix, weights, impacts):
        matrix = np.array(matrix)
        weights = np.array(weights)
        impacts = np.array(impacts)

        norm_matrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))
        weighted_matrix = norm_matrix * weights

        ideal_solution = np.max(weighted_matrix, axis=0) * (impacts == '+') + np.min(weighted_matrix, axis=0) * (impacts == '-')
        negative_ideal_solution = np.min(weighted_matrix, axis=0) * (impacts == '+') + np.max(weighted_matrix, axis=0) * (impacts == '-')

        distance_to_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1))
        distance_to_negative_ideal = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1))

        score = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)
        
        return score
