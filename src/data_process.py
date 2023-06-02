from collections import defaultdict
from random import randint, random, shuffle, sample
from copy import deepcopy
import pandas as pd
from .data_structure import Machine, Job
class GA:
    def __init__(self, matrix, operation_machine_num):
        self.matrix = matrix
        self.operation_machine_num = operation_machine_num
        self.op_num = len(self.operation_machine_num)
        self.job_num = len(self.matrix)
        self.populationnumber = 200
        self.machine_dict = dict()
        self.job_dict = dict()
        self.sol_group = dict()
        self.sol_group_fitness = dict()

    def get_earliset_avl_machine(self, op):
        op_machines = self.machine_dict[op]
        earliset_avl_time = float('inf')
        machine_label = None
        for m_id, machine in op_machines.items():
            if machine.avl_time < earliset_avl_time:
                machine_label = m_id
                earliset_avl_time = machine.avl_time
        return machine_label

    def initialize_machine_dict(self):
        # Initialize machines
        machine_dict = defaultdict(dict)

        for i, num in enumerate(self.operation_machine_num):
            for j in range(num):
                machine_j = Machine(op=i, order=j)
                machine_dict[i][j] = machine_j

        self.machine_dict = machine_dict

    def initialize_job_dict(self):
        # Initialize jobs
        job_dict = {}
        for i in range(self.job_num):
            job = Job(id=i)
            job_dict[i] = job
        self.job_dict = job_dict

    def generate_schedule(self, job_seq):
        # Get schedule of job_seq solution
        for op in range(self.op_num):
            for job_id in job_seq:
                job = self.job_dict[job_id]
                avl_machine_id = self.get_earliset_avl_machine(op)
                avl_machine = self.machine_dict[op][avl_machine_id]

                start_time = max(avl_machine.avl_time, job.last_finish_time)
                work_dur = self.matrix[job_id][op]

                # arrange schedule
                i = 0
                while i < work_dur:
                    avl_machine.schedule[start_time + i] = job_id
                    job.schedule[start_time + i] = op
                    i += 1

                # update avl time
                avl_machine.avl_time = start_time + work_dur
                job.last_finish_time = start_time + work_dur

    def calculate_fitness(self, job_seq):
        last_job_id = job_seq[-1]
        last_job = self.job_dict[last_job_id]
        makespan = max(last_job.schedule.keys()) + 1
        fitness = 1 / makespan if makespan != 0 else 0
        return fitness

    def generate_fitness(self, job_seq):
        self.initialize_machine_dict()
        self.initialize_job_dict()
        self.generate_schedule(job_seq)
        return self.calculate_fitness(job_seq)

    def initialize_sol_group(self):
        # 首先生成一个工件个数的全排列的个体种群，记录在sol_group中
        sol_group = defaultdict(list)
        for i in range(self.populationnumber):
            for j in range(self.job_num):
                sol_group[i].append(j)

        # 将全排列的个体中随机选取两个基因位交换，重复工件个数次，以形成随机初始种群；
        for i in range(self.populationnumber):
            for j in range(self.job_num):
                flg1 = randint(1, self.job_num * 100) % self.job_num
                flg2 = randint(1, self.job_num * 100) % self.job_num
                sol_group[i][flg1], sol_group[i][flg2] = sol_group[i][flg2], sol_group[i][flg1]
        self.sol_group = sol_group
    def calculate_sol_group_fitness(self):
        sol_group_fitness = dict()
        for idx, sol in self.sol_group.items():
            fitness = self.generate_fitness(job_seq=sol)
            sol_group_fitness[idx] = fitness
        self.sol_group_fitness = sol_group_fitness

    def get_best_sol(self):
        sol_group_fitness_sorted = dict(sorted(self.sol_group_fitness.items(), key=lambda k: k[1], reverse=True))
        key = list(sol_group_fitness_sorted.keys())[0]
        return key, self.sol_group[key]
    def select(self):
        # 根据fitness进行自然选择，生成新的种群
        sol_group_fitness = self.sol_group_fitness

        total_fitness = sum(sol_group_fitness.values())
        pro_single = dict()  # 计算每个个体适应度与总体适应度之比；
        roulette = {0: 0} # 将每个个体的概率累加，构造轮盘赌；
        for i in range(self.populationnumber):
            pro_single[i] = sol_group_fitness[i]/total_fitness
            roulette[i + 1] = roulette[i] + pro_single[i]

        updated_sol_group = deepcopy(self.sol_group)
        for i in range(self.populationnumber):
            p = random()
            pin = None
            for j in range(self.populationnumber):
                if (p >= roulette[j] and p < roulette[j+1]):
                    pin = j
                    break
            updated_sol_group[i] = deepcopy(self.sol_group[pin])

        self.sol_group = updated_sol_group

    def get_pairs(self):
        # 将种群中的个体进行两两配对
        population_keys = list(self.sol_group.keys())
        shuffle(population_keys)
        steps = list(range(0, self.populationnumber, 2))
        pairs = [population_keys[i:i + 2] for i in steps]
        return pairs

    def generate_child(self, main_parent, sub_parent, pos1, pos2):
        child = {k: None for k in range(self.job_num)}

        for i in range(pos1, pos2 + 1):  # 从main_parent继承主要信息
            child[i] = main_parent[i]

        none_keys = [k for k, v in child.items() if v is None]  # 剩下的信息从sub_parent继承
        for key in none_keys:
            for v in sub_parent:
                if v not in child.values():
                    child[key] = v
                    break

        return list(child.values())
    def crossover(self):
        updated_sol_group = dict()  # 记录子代的种群
        pairs = self.get_pairs()
        for (idx1, idx2) in pairs:
            parent1 = self.sol_group[idx1]
            parent2 = self.sol_group[idx2]
            (pos1, pos2) = sorted(sample(range(self.job_num), 2))

            child1 = self.generate_child(main_parent=parent2, sub_parent=parent1, pos1=pos1, pos2=pos2)
            child2 = self.generate_child(main_parent=parent1, sub_parent=parent2, pos1=pos1, pos2=pos2)
            updated_sol_group[idx1] = child1
            updated_sol_group[idx2] = child2
        updated_sol_group = dict(sorted(updated_sol_group.items(), key=lambda sol: sol[0]))
        self.sol_group = updated_sol_group

    def mutation(self):
        updated_sol_group = dict()  # 记录变异后的种群
        for i in range(self.populationnumber):
            sol = self.sol_group[i]
            (pos1, pos2) = sorted(sample(range(self.job_num), 2))
            sol[pos1], sol[pos2] = sol[pos2], sol[pos1]
            updated_sol_group[i] = sol
        self.sol_group = updated_sol_group

    # output
    def output_sol(self):
        record_dict = {}
        makespan = max(job.last_finish_time for j_id, job in self.job_dict.items())

        for op_id, machines in self.machine_dict.items():
            for m_id, machine in machines.items():
                machine_id = '工序{0} 机器{1}'.format(op_id, m_id)
                record = {k: '' for k in range(makespan)}
                record.update(machine.schedule)
                record_dict[machine_id] = record

        df = pd.DataFrame(record_dict, dtype=object)
        df.to_csv('output.csv', index=False)


