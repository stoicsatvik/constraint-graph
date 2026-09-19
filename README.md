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
