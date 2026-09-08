import unittest

from constraint_graph import Constraint, ConstraintGraph


class ConstraintGraphTests(unittest.TestCase):
    def test_binding_cut_and_throughput(self):
        graph = ConstraintGraph([
            Constraint("source", "prep", 10),
            Constraint("prep", "pack", 4),
            Constraint("pack", "sink", 9),
        ])
        result = graph.throughput("source", "sink")
        self.assertEqual(result.throughput, 4)
        self.assertEqual(result.binding_constraints, (Constraint("prep", "pack", 4),))

    def test_cycle_is_supported_and_deterministic(self):
        graph = ConstraintGraph([
            Constraint("s", "a", 5),
            Constraint("a", "b", 5),
            Constraint("b", "a", 1),
            Constraint("b", "t", 3),
        ])
        first = graph.throughput("s", "t")
        second = graph.throughput("s", "t")
        self.assertEqual(first, second)
        self.assertEqual(first.throughput, 3)
        self.assertEqual(first.binding_constraints, (Constraint("b", "t", 3),))

    def test_capacity_sensitivity_identifies_useful_relief(self):
        bottleneck = Constraint("prep", "pack", 4)
        graph = ConstraintGraph([
            Constraint("source", "prep", 10),
            bottleneck,
            Constraint("pack", "sink", 9),
        ])
        result = graph.sensitivity("source", "sink", bottleneck, 2)
        self.assertEqual(result.baseline_throughput, 4)
        self.assertEqual(result.changed_throughput, 6)
        self.assertEqual(result.delta_throughput, 2)

    def test_capacity_sensitivity_exposes_nonbinding_change(self):
        nonbinding = Constraint("source", "prep", 10)
        graph = ConstraintGraph([
            nonbinding,
            Constraint("prep", "pack", 4),
            Constraint("pack", "sink", 9),
        ])
        result = graph.sensitivity("source", "sink", nonbinding, 5)
        self.assertEqual(result.delta_throughput, 0)

    def test_parallel_constraints_fail_closed(self):
        with self.assertRaises(ValueError):
            ConstraintGraph([
                Constraint("a", "b", 1),
                Constraint("a", "b", 2),
            ])

    def test_invalid_capacity_change_fails_closed(self):
        edge = Constraint("a", "b", 1)
        graph = ConstraintGraph([edge])
        with self.assertRaises(ValueError):
            graph.sensitivity("a", "b", edge, -2)


if __name__ == "__main__":
    unittest.main()
