import numpy as np
import math

# Indexes of states:
# fair: 0   loaded: 1
initial_probabilities = np.array([0.5,0.5])

# Transition matrix:
# fair-fair     fair-loaded
# loaded-fair   loaded-loaded
transitions_probabilities = np.array([[0.95,0.05], 
                                      [0.1 ,0.9 ]])

# Emission matrix:
# fair-1 ... fair-6
# loaded-1 ... loaded-6
emission_probabilities = np.array([[1/6,1/6,1/6,1/6,1/6,1/6],
                                   [0.1,0.1,0.1,0.1,0.1,0.5]])

# Converting the probabilities to log in base 2:
for i in range(0,2):
    initial_probabilities[i] = math.log(initial_probabilities[i], 2) 
for i in range(0,2):
    for j in range(0,2):
        transitions_probabilities[i,j] = math.log(transitions_probabilities[i,j], 2) 
for i in range(0,2):
    for j in range(0,6):
        emission_probabilities[i,j] = math.log(emission_probabilities[i,j], 2) 
# Checking:
print("\nProbabilities in log values:")
print(initial_probabilities)
print(transitions_probabilities)
print(emission_probabilities)

# Receives a sequence and presents the best solution
def viterbi(sequence):

    print("\n---------")
    print("\nSequence:")
    print (sequence)

    n_emissions = sequence.size
    n_states = 2

    viterbi_matrix = np.zeros((n_states, n_emissions))
    states_solutions = np.zeros((n_states, n_emissions))

    for j in range(0,n_emissions):  # emissions
        for i in range(0,n_states):  # states

            index_emitted_value = sequence[j] - 1
            if j == 0:
                viterbi_matrix[i,j] = initial_probabilities[i] + emission_probabilities[i,index_emitted_value]
            else:
                fair_origin_value = viterbi_matrix[0,j-1] + transitions_probabilities[0,i] + emission_probabilities[i,index_emitted_value]
                loaded_origin_value = viterbi_matrix[1,j-1] + transitions_probabilities[1,i] + emission_probabilities[i,index_emitted_value]
                
                if fair_origin_value >= loaded_origin_value:
                    viterbi_matrix[i,j] = fair_origin_value
                    states_solutions[i,j-1] = 0
                else:  
                    viterbi_matrix[i,j] = loaded_origin_value
                    states_solutions[i,j-1] = 1

    states_solutions[0,n_emissions-1] = 0
    states_solutions[1,n_emissions-1] = 1

    print("\nViterbi matrix:")
    print (viterbi_matrix)

    print("\nSolutions: (0: fair; 1: loaded)")
    print (states_solutions)

    print("\nBest solution:")
    if viterbi_matrix[0,n_emissions-1] >= viterbi_matrix[1,n_emissions-1]:
        print(states_solutions[0])
    else:
        print(states_solutions[1])

# Testing:
sequence = np.array([6,4,1,2])
viterbi(sequence)

sequence = np.array([6,6,4,1,2])
viterbi(sequence)

sequence = np.array([6,4,1,2,6])
viterbi(sequence)

sequence = np.array([1,2,3,4,6,6,6,1,2,3])
viterbi(sequence)
