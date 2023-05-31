
class Machine:
    def __init__(self, op, order):
        self.operation = op
        self.order = order
        self.avl_time = 0
        self.schedule = {}


    def __repr__(self):
        return "Machine(op={0}, order={1})".format(self.operation, self.order)


class Job:
    def __init__(self, id):
        self.id = id
        self.last_finish_time = 0
        self.schedule = {}

    def __repr__(self):
        return "Job(id={0})".format(self.id)