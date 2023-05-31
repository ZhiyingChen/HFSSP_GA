from collections import defaultdict
from data_structure import Machine, Job
from data_process import Input
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

# op_num = len(operation_machine_num)
# job_num = len(matrix)
#
#
# def get_earliset_avl_machine(op_machines):
#     earliset_avl_time = float('inf')
#     machine_label = None
#     for m_id, machine in op_machines.items():
#         if machine.avl_time < earliset_avl_time:
#             machine_label = m_id
#             earliset_avl_time = machine.avl_time
#     return machine_label
#
#
# # Initialize machines
# machine_dict = defaultdict(dict)
#
# for i, num in enumerate(operation_machine_num):
#     for j in range(num):
#         machine_j = Machine(op=i, order=j)
#         machine_dict[i][j] = machine_j
#
# # Initialize jobs
# job_dict = {}
# for i in range(job_num):
#     job = Job(id=i)
#     job_dict[i] = job
#
# job_seq = [0, 1, 2, 3, 4, 5]
# for op in range(op_num):
#     op_machines = machine_dict[op]
#     for job_id in job_seq:
#         job = job_dict[job_id]
#         avl_machine_id = get_earliset_avl_machine(op_machines)
#         avl_machine = op_machines[avl_machine_id]
#
#         start_time = max(avl_machine.avl_time, job.last_finish_time)
#         work_dur = matrix[job_id][op]
#
#         # arrange schedule
#         i = 0
#         while i < work_dur:
#             avl_machine.schedule[start_time + i] = job_id
#             job.schedule[start_time + i] = op
#             i += 1
#
#         # update avl time
#         avl_machine.avl_time = start_time + work_dur
#         job.last_finish_time = start_time + work_dur

sol = [0, 1, 2, 3, 4, 5]
input = Input(matrix, operation_machine_num)
fitness = input.generate_fitness(job_seq=sol)







