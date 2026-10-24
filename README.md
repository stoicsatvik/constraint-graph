# constraint-graph

A dependency-free Python primitive for representing capacity constraints and finding system bottlenecks reproducibly.

```python
from constraint_graph import Constraint, ConstraintGraph

g = ConstraintGraph([
    Constraint("orders", "assembly", 12, "assembly"),
    Constraint("assembly", "shipping", 7, "shipping"),
])

assert g.max_throughput("orders", "shipping") == 7
print(g.binding_constraints("orders", "shipping"))
print(g.sensitivity("orders", "shipping"))
```

`max_throughput` uses deterministic Edmonds-Karp max flow and supports directed cycles. `sensitivity` increases one capacity at a time and recomputes system throughput; `binding_constraints` returns only edges whose isolated increase improves throughput.

## Claim boundary

This library computes consequences of the graph and capacities supplied to it. It does **not** infer whether a real-world model is complete, causal, correctly measured, or strategically important. A reported binding constraint is therefore conditional on the input model.

## Test

```bash
python -m unittest discover -s tests -v
```

## Numerical boundary

Constraint capacities and sensitivity deltas must be finite; invalid inputs fail closed. Binding edges are identified only when their isolated throughput gain exceeds an **8-ULP scale-aware numerical tolerance**, rather than an absolute unit threshold. Gains smaller than the available floating-point resolution are not certified as binding. The max-flow solver is checked against an independent exhaustive min-cut oracle on small scaled synthetic graphs; this does not validate external resource-capacity measurements.
