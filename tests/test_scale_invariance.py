"""Independent min-cut oracle and floating-scale adversarial tests."""
import itertools
import math
import random
import unittest
from constraint_graph import Constraint, ConstraintGraph


def min_cut_oracle(edges, source="s", sink="t"):
    # Exhaustively enumerate every source/sink cut on four-node graphs.
    nodes = sorted(({e.source for e in edges} | {e.target for e in edges}) - {source, sink})
    best = float("inf")
    for bits in itertools.product((False, True), repeat=len(nodes)):
        left = {source} | {node for node, take in zip(nodes, bits) if take}
        cost = math.fsum(e.capacity for e in edges if e.source in left and e.target not in left)
        best = min(best, cost)
    return best


class ScaleFalsification(unittest.TestCase):
    def test_nonfinite_capacities_fail_closed(self):
        for bad in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Constraint("s", "t", bad)
        with self.assertRaises(ValueError):
            Constraint(42, "t", 1)

    def test_nonfinite_sensitivity_delta_fails_closed(self):
        graph = ConstraintGraph([Constraint("s", "t", 1)])
        for bad in (float("nan"), float("inf"), -float("inf"), 0):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                graph.sensitivity("s", "t", delta=bad)

    def test_tiny_binding_cut_is_not_lost_to_absolute_threshold(self):
        for scale in (1e-15, 1e-12, 1.0, 1e12):
            graph = ConstraintGraph([Constraint("s", "a", 2 * scale, "upstream"), Constraint("a", "t", scale, "binding")])
            with self.subTest(scale=scale):
                self.assertEqual(graph.max_throughput("s", "t"), scale)
                self.assertEqual([e.name for e in graph.binding_constraints("s", "t", delta=scale)], ["binding"])

    def test_independent_exhaustive_min_cut_across_scales(self):
        rng = random.Random(20261024)
        for trial in range(80):
            edges = []
            for u, v in itertools.permutations(("s", "a", "b", "t"), 2):
                if rng.random() < 0.52:
                    edges.append((u, v, rng.randrange(0, 6)))
            if not edges:
                continue
            if not any(u == "s" for u, _, _ in edges) or not any(v == "t" for _, v, _ in edges):
                continue
            for scale in (1e-15, 1.0, 1e12):
                model = [Constraint(u, v, cap * scale) for u, v, cap in edges]
                graph = ConstraintGraph(model)
                expected = min_cut_oracle(model)
                actual = graph.max_throughput("s", "t")
                with self.subTest(trial=trial, scale=scale):
                    self.assertTrue(math.isclose(actual, expected, rel_tol=1e-11, abs_tol=0), (actual, expected))


if __name__ == "__main__":
    unittest.main()
