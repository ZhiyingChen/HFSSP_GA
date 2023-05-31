from collections import defaultdict
from data_structure import Machine, Job

class Input:
    def __init__(self, matrix, operation_machine_num):
        self.matrix =matrix
        self.operation_machine_num = operation_machine_num
        self.op_num = len(self.operation_machine_num)
        self.job_num = len(self.matrix)
        self.machine_dict = dict()
        self.job_dict = dict()

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

    def get_fitness(self, job_seq):
        last_job_id = job_seq[-1]
        last_job = self.job_dict[last_job_id]
        max_time = max(last_job.schedule.keys()) + 1
        fitness = 1 / max_time if max_time != 0 else 0
        return fitness

    def generate_fitness(self, job_seq):
        self.initialize_machine_dict()
        self.initialize_job_dict()
        self.generate_schedule(job_seq)
        return self.get_fitness(job_seq)

