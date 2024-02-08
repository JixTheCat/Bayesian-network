import itertools
import numpy as np

# Edge ranking method
# We give each edge a ranking and normalise from best to worst scenario.

def calculate_LH(x_L, x_H, weights):
    """Given the best and worst case scenarios, x_L and x_H, we calculate the unit weight for the CPT."""
    return x_L/sum(weights), x_H/sum(weights)

def combinations(num_weights):
    return list(itertools.product([False, True], repeat=num_weights))

def create_boolean_matrix(x_L, x_H, num_weights):
    # Generate all possible combinations of True and False for the given number
    all_combinations = combinations(num_weights)
    # Create a boolean matrix with each combination as a row
    boolean_matrix = [[x_L if bit else x_H for bit in combination] for combination in all_combinations]

    return np.array(boolean_matrix)

def calculate_CPT(weights, x_L, x_H):
    boolean_matrix = create_boolean_matrix(
        *calculate_LH(x_L, x_H, weights),
        len(weights)
    )

    return sum(np.transpose(np.array([weights]*len(boolean_matrix))*boolean_matrix))

# Counts method:
# We give everything the same weighting and determine the
# COT through the number of occurences of Low/Highs
def counts_CPT(weights: dict):
    # For this example we are count the number of occurences of low/bad/no/etc
    all_combinations = combinations(len(weights)-1)
    return [weights.get(value, value) for value in sum(np.transpose(np.array(all_combinations)))]

if __name__ == "__main__":
    weights = [1, 2]
    x_L = 0.1
    x_H = 0.9
    matrix = calculate_CPT(weights, x_L, x_H)
    np.savetxt("low", matrix, newline='\t', fmt="%1f")
    np.savetxt("high", 1-matrix, newline='\t', fmt="%1f")
