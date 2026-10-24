# Foundry State

## Objective
Build a small, rigorous library for representing resources, constraints, capacities, dependencies, and bottlenecks as graphs, then computing which constraints currently limit throughput.

## Public boundary
This repo contains generic modeling primitives only. Do not add proprietary strategy scoring, private business data, Mumbai Traffic logic, or private cross-project intelligence.

## V0 milestone
- Typed graph schema for resources/nodes and constraints/edges
- Bottleneck detection on directed acyclic and cyclic examples
- Sensitivity analysis: how throughput changes when one capacity changes
- Deterministic examples and tests
- Minimal CLI or Python API

## Acceptance
A stranger can model a toy supply chain or process in <20 lines and obtain the binding constraint plus a reproducible sensitivity report.

## Next move
Implement the core graph schema and one deterministic max-throughput/bottleneck example before adding visualization.

Status: ACTIVE / NOT YET PROVEN

## 2026-10-24: E222 independent min-cut / floating-scale falsification

**Branch:** `foundry/e222-scale-invariant-cut-audit-20261024`, stacked draft PR #3 on PR #2. Test-only head `165448bb47bcef5e752f5ea88dc2a65308c19f8b` failed the new regressions in Actions [40099110781](https://github.com/stoicsatvik/constraint-graph/actions/runs/40099110781), as expected. Corrected head `71be23853298fddad25a2e4b503d0dd77ab607ba` passed [40099120568](https://github.com/stoicsatvik/constraint-graph/actions/runs/40099120568).

**Falsified:** The absolute 1e-12 bottleneck threshold hid genuinely binding cuts with capacities 1e-15 and 1e-12. Nonfinite NaN/Inf capacities and deltas were not rejected. **Corrected:** finite input validation, fail-closed nonfinite total flow, and a scale-aware 8-ULP bottleneck decision. Independent exhaustive min-cut oracle agreed with Edmonds–Karp on **204 deterministic small directed/cyclic/antiparallel scaled graph cases** at 1e-15, 1 and 1e12. This validates a narrow algorithmic invariant only, not causal model completeness or real-world bottleneck truth.

**Next:** randomized larger-graph min-cut oracle and cancellation/overflow stress, then an externally supplied toy supply-chain model. No production deployment or main merge.
