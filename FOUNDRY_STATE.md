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

## Current challenger
Branch: `foundry/v0-core-graph`
Draft PR: #1
Implementation head: `7a8134791376eecf20baeb77e0ddc4b15260764c`
Capabilities: typed capacity constraints, deterministic max-throughput, binding min-cut extraction, one-edge capacity sensitivity, cyclic graph support, fail-closed validation, six deterministic contracts, narrow CPU-only CI.
Validation: inspectable implementation and contracts are present; no exact-head workflow run was visible immediately after PR creation.
Claim status: architecture/contracts SUPPORTED; runtime NOT YET PROVEN.

## Blocker
Exact-head CI evidence for `7a8134791376eecf20baeb77e0ddc4b15260764c`.

## Next move
If the core contracts pass, freeze this core as the V0 champion and add a minimal <20-line example/report surface. If they fail, preserve the failure and repair only the violated contract.

Status: ACTIVE / NOT YET PROVEN
