import unittest

from monitor import calculate_backoff_delay


class MonitorHelpersTest(unittest.TestCase):
    def test_backoff_delay_growth_and_cap(self):
        self.assertEqual(calculate_backoff_delay(0, base_delay=1.0, max_delay=8.0), 1.0)
        self.assertEqual(calculate_backoff_delay(1, base_delay=1.0, max_delay=8.0), 2.0)
        self.assertEqual(calculate_backoff_delay(3, base_delay=1.0, max_delay=8.0), 8.0)


if __name__ == "__main__":
    unittest.main()
