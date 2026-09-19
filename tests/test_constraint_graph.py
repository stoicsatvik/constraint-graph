import unittest

from constraint_graph import Constraint, ConstraintGraph


class ConstraintGraphTests(unittest.TestCase):
    def test_toy_supply_chain_finds_binding_edge(self):
        graph = ConstraintGraph([
            Constraint("source", "prep", 10, "intake"),
            Constraint("prep", "sink", 4, "packing"),
        ])
        self.assertEqual(graph.max_throughput("source", "sink"), 4)
        self.assertEqual([e.name for e in graph.binding_constraints("source", "sink")], ["packing"])

    def test_parallel_paths_sum_throughput(self):
        graph = ConstraintGraph([
            Constraint("s", "a", 3), Constraint("a", "t", 3),
            Constraint("s", "b", 5), Constraint("b", "t", 5),
        ])
        self.assertEqual(graph.max_throughput("s", "t"), 8)

    def test_cycle_does_not_break_flow_or_determinism(self):
        graph = ConstraintGraph([
            Constraint("s", "a", 5), Constraint("a", "b", 4),
            Constraint("b", "a", 2), Constraint("b", "t", 4),
            Constraint("a", "t", 1),
        ])
        self.assertEqual(graph.max_throughput("s", "t"), 5)
        self.assertEqual(graph.max_throughput("s", "t"), 5)

    def test_sensitivity_reports_only_real_system_gain(self):
        graph = ConstraintGraph([
            Constraint("s", "a", 10, "upstream"),
            Constraint("a", "t", 3, "downstream"),
        ])
        report = {r.constraint.name: r.marginal_gain for r in graph.sensitivity("s", "t")}
        self.assertEqual(report, {"downstream": 1, "upstream": 0})

    def test_invalid_models_fail_closed(self):
        with self.assertRaises(ValueError):
            Constraint("a", "b", -1)
        with self.assertRaises(ValueError):
            ConstraintGraph([Constraint("a", "b", 1), Constraint("a", "b", 2)])


if __name__ == "__main__":
    unittest.main()
