# pyshpe

Hierarchical Task Networks (HTN) deconstruct a high-level task (e.g. travel from point A to point B) into a sequence of low-level operations (e.g. call a taxi to point A, ride the taxi from point A to point B, pay the taxi diver). The decomposition checks that valid operations are selected for the current world state.

Unlike a classical planner such as STRIPS, HTN planners must capture this decomposition information for each application into their implementation.

This implementation mirrors the techniques of the Simple Hierarchical Planning Engine (SHPE)<sup>1</sup>. This has the following advantages over PyHOP:

1. The algorithm is iterative rather than recursive, which makes limiting the execution time for time-slicing in games or embedded systems easier.
2. The algorithm allows adding a cost function for operations, so an optimum plan may be found.

## Usage

Each task must be inherit `PrimitiveTask` or `CompoundTask`. It is recommended to decorate each class with `@dataclass` to make improve readability.

``` python
@dataclass
class Walk(PrimitiveTask):
    a: str  # Agent that will walk
    x: str  # Origin of agent
    y: str  # Destination of agent

    def applicable(self, state):
        return state.loc[self.a] == self.x

    def apply(self, state):
        state.loc[self.a] = self.y
        return state

@dataclass
class Travel(CompoundTask):
    a: str  # Agent that will travel by some means such as walking or biking
    x: str  # Origin of agent
    y: str  # Destination of agent

    def decompose(self, state):
        a, x, y = self.a, self.x, self.y
        return [[TravelByFoot(a, x, y)], [TravelByTaxi(a, x, y)]]
```

To get the first successful plan, use `find_first_plan`:

``` python
plan, cost = find_first_plan(state, [Travel('me', 'posX', 'posY')])
```

The returned plan will be a list of primitive tasks if successful, and an empty array if not.

To find the optimal plan, use `find_best_plan`:

``` python
plan, cost = find_best_plan(state, [Travel('me', 'posX', 'posY')])
```

## References

1. "SHPE: HTN Planning for Video Games", Alexandre Menif, Eric Jacopin, Tristan Cazenave. Available [online](http://www.lamsade.dauphine.fr/~cazenave/papers/MenifCGW2014.pdf).
