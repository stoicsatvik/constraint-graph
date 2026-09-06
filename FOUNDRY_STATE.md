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
