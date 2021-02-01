# Travel problem based on Pyhop example
from dataclasses import dataclass
from pyshpe import State, PrimitiveTask, CompoundTask, find_first_plan


def taxi_rate(distance):
    return 1.5 * 0.5 * distance


@dataclass
class Walk(PrimitiveTask):
    a: str
    x: str
    y: str

    def applicable(self, state):
        return state.loc[self.a] == self.x

    def apply(self, state):
        state.loc[self.a] = self.y
        return state


@dataclass
class CallTaxi(PrimitiveTask):
    x: str

    def apply(self, state):
        state.loc['taxi'] = self.x
        return state


@dataclass
class RideTaxi(PrimitiveTask):
    a: str
    x: str
    y: str

    def apply(self, state):
        if state.loc['taxi'] == self.x and state.loc[self.a] == self.x:
            state.loc['taxi'] = self.y
            state.loc[self.a] = self.y
            state.owe[self.a] = taxi_rate(state.dist[self.x][self.y])

        return state


@dataclass
class PayDriver(PrimitiveTask):
    a: str

    def apply(self, state):
        if state.cash[self.a] >= state.owe[self.a]:
            state.cash[self.a] = state.cash[self.a] - state.owe[self.a]
            state.owe[self.a] = 0

        return state


@dataclass
class TravelByFoot(CompoundTask):
    a: str
    x: str
    y: str

    def decompose(self, state):
        if state.dist[self.x][self.y] <= 2:
            return [[Walk(self.a, self.x, self.y)]]
        else:
            return []


@dataclass
class TravelByTaxi(CompoundTask):
    a: str
    x: str
    y: str

    def decompose(self, state):
        a, x, y = self.a, self.x, self.y

        if state.cash[a] >= taxi_rate(state.dist[x][y]):
            return [[CallTaxi(x), RideTaxi(a, x, y), PayDriver(a)]]
        else:
            return []


@dataclass
class Travel(CompoundTask):
    a: str
    x: str
    y: str

    def decompose(self, state):
        a, x, y = self.a, self.x, self.y
        return [[TravelByFoot(a, x, y)], [TravelByTaxi(a, x, y)]]


def test_walk():
    state = State()
    state.loc = {'me': 'posX'}
    plan, cost = find_first_plan(state, [Walk('me', 'posX', 'posY')])
    assert type(plan[0]) == Walk

    state.loc = {'me': 'posA'}
    plan, cost = find_first_plan(state, [Walk('me', 'posX', 'posY')])
    assert len(plan) == 0


def test_full_travel_with_cash():
    state = State()
    state.loc = {'me': 'posX', 'taxi': 'cab_stand'}
    state.cash = {'me': 20}
    state.owe = {'me': 0}
    state.dist = {
        'posX': {'posY': 8},
        'posY': {'posX': 8},
    }

    task_network = [Travel('me', 'posX', 'posY')]
    plan, cost = find_first_plan(state, task_network)

    assert len(plan) == 3
    assert type(plan[0]) == CallTaxi
    assert type(plan[1]) == RideTaxi
    assert type(plan[2]) == PayDriver
    assert cost == 3.0


def test_full_travel_without_cash():
    state = State()
    state.loc = {'me': 'posX', 'taxi': 'cab_stand'}
    state.cash = {'me': 0}
    state.owe = {'me': 0}
    state.dist = {
        'posX': {'posY': 1},
        'posY': {'posX': 1},
    }

    task_network = [Travel('me', 'posX', 'posY')]
    plan, cost = find_first_plan(state, task_network)

    assert len(plan) == 1
    assert type(plan[0]) == Walk
    assert cost == 1.0
