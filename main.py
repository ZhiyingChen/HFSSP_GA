from data_process import GA
import random


# parameters
matrix = [
    [2, 4, 6],
    [4, 9, 2],
    [4, 2, 8],
    [9, 5, 6],
    [5, 2, 7],
    [9, 4, 3]
]
operation_machine_num = [2, 2, 2]

iter_num = 100
mutation_rate = 0.05
crossover_rate = 0.6

# generate initial group
input = GA(matrix, operation_machine_num)
input.initialize_sol_group()

# iterrate to run genetic algorithm
for i in range(iter_num):
    input.calculate_sol_group_fitness()
    input.select()
    p = random.random()
    if p <= crossover_rate:
        input.crossover()
    if p <= mutation_rate:
        input.mutation()

# calculate fitnes of final group solutions
input.calculate_sol_group_fitness()
key, best_sol = input.get_best_sol()

# generate schedule of best sol
input.initialize_machine_dict()
input.initialize_job_dict()
input.generate_schedule(job_seq=best_sol)






