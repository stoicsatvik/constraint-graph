"""Small dependency-free capacity graph with reproducible throughput analysis."""
from __future__ import annotations

from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True, order=True)
class Constraint:
    source: str
    target: str
    capacity: float
    name: str = ""

    def __post_init__(self) -> None:
        if not self.source or not self.target:
            raise ValueError("constraint endpoints must be non-empty")
        if self.source == self.target:
            raise ValueError("self-loops are not supported")
        if self.capacity < 0:
            raise ValueError("capacity must be non-negative")


@dataclass(frozen=True)
class Sensitivity:
    constraint: Constraint
    baseline_throughput: float
    perturbed_throughput: float

    @property
    def marginal_gain(self) -> float:
        return self.perturbed_throughput - self.baseline_throughput


class ConstraintGraph:
    def __init__(self, constraints: list[Constraint] | tuple[Constraint, ...]) -> None:
        if not constraints:
            raise ValueError("at least one constraint is required")
        keys = [(c.source, c.target) for c in constraints]
        if len(keys) != len(set(keys)):
            raise ValueError("parallel edges are ambiguous; aggregate them first")
        self.constraints = tuple(sorted(constraints))
        self.nodes = frozenset({n for c in constraints for n in (c.source, c.target)})

    def max_throughput(self, source: str, sink: str) -> float:
        """Return deterministic max flow using Edmonds-Karp; cycles are supported."""
        self._validate_terminals(source, sink)
        residual: dict[tuple[str, str], float] = {}
        adjacency: dict[str, set[str]] = {n: set() for n in self.nodes}
        for edge in self.constraints:
            residual[(edge.source, edge.target)] = edge.capacity
            residual.setdefault((edge.target, edge.source), 0.0)
            adjacency[edge.source].add(edge.target)
            adjacency[edge.target].add(edge.source)

        total = 0.0
        while True:
            parent: dict[str, str | None] = {source: None}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for v in sorted(adjacency[u]):
                    if v not in parent and residual.get((u, v), 0.0) > 0:
                        parent[v] = u
                        queue.append(v)
            if sink not in parent:
                return total
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
                residual[(v, u)] = residual.get((v, u), 0.0) + path_capacity
                v = u
            total += path_capacity

    def sensitivity(self, source: str, sink: str, *, delta: float = 1.0) -> tuple[Sensitivity, ...]:
        """Increase each edge by ``delta`` independently and report throughput change."""
        if delta <= 0:
            raise ValueError("delta must be positive")
        baseline = self.max_throughput(source, sink)
        reports: list[Sensitivity] = []
        for edge in self.constraints:
            changed = [
                Constraint(c.source, c.target, c.capacity + delta if c == edge else c.capacity, c.name)
                for c in self.constraints
            ]
            perturbed = ConstraintGraph(changed).max_throughput(source, sink)
            reports.append(Sensitivity(edge, baseline, perturbed))
        return tuple(reports)

    def binding_constraints(self, source: str, sink: str, *, delta: float = 1.0) -> tuple[Constraint, ...]:
        """Return edges whose isolated capacity increase raises system throughput."""
        return tuple(r.constraint for r in self.sensitivity(source, sink, delta=delta) if r.marginal_gain > 1e-12)

    def _validate_terminals(self, source: str, sink: str) -> None:
        if source == sink:
            raise ValueError("source and sink must differ")
        if source not in self.nodes or sink not in self.nodes:
            raise ValueError("source and sink must be graph nodes")
