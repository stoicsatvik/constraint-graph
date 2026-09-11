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

## Current champion candidate
Branch: `foundry/v0-core-graph`
Draft PR: #1
Tested implementation head: `bebba4fa408244418cf75030812726a677be271b`
Capabilities: typed capacity constraints, deterministic max-throughput, binding min-cut extraction, one-edge sensitivity, deterministic all-edge sensitivity ranking, cyclic graph support, fail-closed validation, <20-line toy-process example, narrow CPU-only CI.
Validation: GitHub Actions run `34555037075`, job `103125775323`, CPython 3.12.14, passed 9/9 deterministic contracts in 0.082 s. The all-edge report contract verifies useful-relief ranking, preserves zero-gain non-binding edges as controls, repeats deterministically, and rejects non-positive probe sizes.
Claim status: V0 synthetic graph core and deterministic sensitivity-report surface SUPPORTED. Real-world bottleneck or causal operational claims NOT YET PROVEN.

## Blocker
No V0 evidence blocker. PR remains draft/unmerged pending explicit approval. External usefulness/adoption is not yet established.

## Next move
Freeze this V0 surface unless users expose a concrete gap. Highest-EV future work is a fresh, deterministic multi-bottleneck fixture that tests whether one-edge sensitivity can mislead when relief must be coordinated across multiple constraints; do not add visualization or domain-specific logic before that falsification case.

Status: ACTIVE / SUPPORTED V0
