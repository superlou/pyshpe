import logging
from copy import deepcopy
from dataclasses import dataclass


class State():
    pass


# @dataclass
class Task():
    pass
    # def __init__(self, *args):
    #     try:
    #         for parameter, value in zip(self.parameters.split(' '), args):
    #             setattr(self, parameter, value)
    #     except AttributeError:
    #         pass


class PrimitiveTask(Task):
    """Tasks are primitive operations"""

    def applicable(self, state) -> bool:
        return True

    def apply(self, state) -> State:
        return state

    def cost(self, state) -> float:
        return 1.0

    # def __str__(self) -> str:
    #     return f'{type(self).__name__}'


class CompoundTask(Task):
    """ Compound tasks must be decomposed"""

    def decompose(self, state) -> []:
        return []

    # def __str__(self) -> str:
    #     return f'({type(self).__name__})'


def replace_with_array(a, i, replacing_array):
    return a[:i] + replacing_array + a[i + 1:]


def shpe_next(stack, best_plan, best_cost):
    plan, cost, state, task_network = stack.pop(0)
    logging.info('Running next')
    logging.info('Task Network: ' + ', '.join([str(t) for t in task_network]))
    logging.info('Plan: ' + ', '.join([str(t) for t in plan]))
    logging.info('Cost: ' + str(cost))

    if cost >= best_cost:
        return best_plan, best_cost

    if len(task_network) == 0:
        return plan, cost

    # Assume that the first task is the only one without predecessor
    task = task_network[0]

    if isinstance(task, PrimitiveTask):
        if task.applicable(state):
            plan.append(task)
            cost += task.cost(state)

            new_tn = task_network[1:].copy()
            stack.insert(0, (plan, cost, task.apply(deepcopy(state)), new_tn))
    elif isinstance(task, CompoundTask):
        for tn in task.decompose(state):
            new_tn = tn + task_network[1:].copy()
            stack.insert(0, (plan, cost, deepcopy(state), new_tn))


def find_first_plan(state, task_network):
    stack = []
    best_plan = []
    best_cost = 1e9  # todo Why doesn't float('inf') work?

    stack.append(([], 0, state, task_network))

    while best_cost == 1e9 and len(stack) > 0:
        result = shpe_next(stack, best_plan, best_cost)
        if result:
            best_plan, best_cost = result

    return best_plan, best_cost


def find_best_plan(state, task_network):
    stack = []
    best_plan = []
    best_cost = 1e9  # todo Why doesn't float('inf') work?

    stack.insert(0, ([], 0, state, task_network))

    while len(stack) > 0:
        result = shpe_next(stack, best_plan, best_cost)
        if result:
            best_plan, best_cost = result

    return best_plan, best_cost
