import subprocess
import sys
import unittest
from pathlib import Path


class ExampleContractTests(unittest.TestCase):
    def test_toy_process_is_small_and_reproducible(self):
        path = Path("examples/toy_process.py")
        active = [line for line in path.read_text().splitlines() if line.strip() and not line.lstrip().startswith("#")]
        self.assertLessEqual(len(active), 20)

        expected = "throughput=9.0\nbinding=prep->finish\n+1 capacity => +1.0 throughput\n"
        first = subprocess.check_output([sys.executable, str(path)], text=True)
        second = subprocess.check_output([sys.executable, str(path)], text=True)
        self.assertEqual(first, expected)
        self.assertEqual(second, expected)


if __name__ == "__main__":
    unittest.main()
