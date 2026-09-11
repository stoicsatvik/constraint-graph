from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Hashable, Iterable

Node = Hashable


@dataclass(frozen=True, order=True)
class Constraint:
    source: Node
    target: Node
    capacity: float

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise ValueError("self-loop constraints are not supported")
        if self.capacity < 0:
            raise ValueError("capacity must be non-negative")


@dataclass(frozen=True)
class ThroughputResult:
    throughput: float
    binding_constraints: tuple[Constraint, ...]


@dataclass(frozen=True)
class SensitivityResult:
    constraint: Constraint
    delta_capacity: float
    baseline_throughput: float
    changed_throughput: float

    @property
    def delta_throughput(self) -> float:
        return self.changed_throughput - self.baseline_throughput


class ConstraintGraph:
    def __init__(self, constraints: Iterable[Constraint]) -> None:
        self.constraints = tuple(constraints)
        if not self.constraints:
            raise ValueError("graph requires at least one constraint")
        pairs = [(c.source, c.target) for c in self.constraints]
        if len(pairs) != len(set(pairs)):
            raise ValueError("parallel constraints are not supported in v0")

    def throughput(self, source: Node, sink: Node) -> ThroughputResult:
        if source == sink:
            raise ValueError("source and sink must differ")
        nodes = {n for c in self.constraints for n in (c.source, c.target)}
        if source not in nodes or sink not in nodes:
            raise ValueError("source and sink must exist in the graph")

        residual: dict[tuple[Node, Node], float] = {}
        adjacency: dict[Node, set[Node]] = {n: set() for n in nodes}
        for c in self.constraints:
            residual[(c.source, c.target)] = float(c.capacity)
            residual.setdefault((c.target, c.source), 0.0)
            adjacency[c.source].add(c.target)
            adjacency[c.target].add(c.source)

        flow = 0.0
        while True:
            parent: dict[Node, Node | None] = {source: None}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for v in sorted(adjacency[u], key=repr):
                    if v not in parent and residual[(u, v)] > 0:
                        parent[v] = u
                        queue.append(v)
            if sink not in parent:
                break

            path_capacity = float("inf")
            v = sink
            while parent[v] is not None:
                u = parent[v]
                path_capacity = min(path_capacity, residual[(u, v)])
                v = u
            v = sink
            while parent[v] is not None:
                u = parent[v]
                residual[(u, v)] -= path_capacity
                residual[(v, u)] += path_capacity
                v = u
            flow += path_capacity

        reachable = {source}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in sorted(adjacency[u], key=repr):
                if v not in reachable and residual[(u, v)] > 0:
                    reachable.add(v)
                    queue.append(v)

        binding = tuple(
            sorted(
                (c for c in self.constraints if c.source in reachable and c.target not in reachable),
                key=lambda c: (repr(c.source), repr(c.target), c.capacity),
            )
        )
        return ThroughputResult(flow, binding)

    def sensitivity(
        self, source: Node, sink: Node, constraint: Constraint, delta_capacity: float
    ) -> SensitivityResult:
        if constraint not in self.constraints:
            raise ValueError("constraint must belong to the graph")
        new_capacity = constraint.capacity + delta_capacity
        if new_capacity < 0:
            raise ValueError("capacity change would make capacity negative")
        baseline = self.throughput(source, sink).throughput
        changed_constraints = tuple(
            Constraint(c.source, c.target, new_capacity) if c == constraint else c
            for c in self.constraints
        )
        changed = ConstraintGraph(changed_constraints).throughput(source, sink).throughput
        return SensitivityResult(constraint, delta_capacity, baseline, changed)

    def sensitivity_report(
        self, source: Node, sink: Node, delta_capacity: float = 1.0
    ) -> tuple[SensitivityResult, ...]:
        if delta_capacity <= 0:
            raise ValueError("report delta_capacity must be positive")
        results = (
            self.sensitivity(source, sink, constraint, delta_capacity)
            for constraint in self.constraints
        )
        return tuple(
            sorted(
                results,
                key=lambda result: (
                    -result.delta_throughput,
                    repr(result.constraint.source),
                    repr(result.constraint.target),
                    result.constraint.capacity,
                ),
            )
        )
