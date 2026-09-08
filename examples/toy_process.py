import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from constraint_graph import Constraint, ConstraintGraph

edges = [
    Constraint("source", "prep", 12),
    Constraint("prep", "finish", 7),
    Constraint("source", "finish", 2),
]
graph = ConstraintGraph(edges)
result = graph.throughput("source", "finish")
binding = result.binding_constraints[0]
sensitivity = graph.sensitivity("source", "finish", binding, 1)

print(f"throughput={result.throughput:.1f}")
print(f"binding={binding.source}->{binding.target}")
print(f"+1 capacity => +{sensitivity.delta_throughput:.1f} throughput")
