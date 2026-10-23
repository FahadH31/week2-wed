"""
test_run_stats.py -- Part C: your unit tests for run_stats.py.

Run from the starter_code folder:
    python -m unittest -v test_run_stats

Requirements (see README, Part C):
  * at least 12 test methods
  * one regression test for each of the 7 bugs (a test that FAILS on the buggy file and PASSES once fixed)
  * at least 3 tests of bad or unusual input (empty list, n == 0, missing key)
  * at least 1 test that uses assertRaises
  * at least 1 use of setUp (so tests stay independent) and at least 1 use of assertLogs (Part B)
Name every test for the behaviour it protects, e.g. test_even_count_averages_two_middle_values.
"""
import unittest

import run_stats


class TestMedian(unittest.TestCase):
    # Worked example: Arrange, Act, Assert.
    def test_odd_count_returns_middle(self):
        values = [5, 1, 3]                       # Arrange
        result = run_stats.median(values)        # Act
        self.assertEqual(result, 3)              # Assert

    def test_even_count_averages_two_middle_values(self):
        # BUG-1: median of even list should average middle two
        values = [4, 1, 3, 2]
        result = run_stats.median(values)
        self.assertAlmostEqual(result, 2.5)

    def test_empty_list_raises_value_error(self):
        # BUG-7: empty list must raise ValueError
        with self.assertRaises(ValueError):
            run_stats.median([])

    def test_median_input_list_not_changed(self):
        values = [4, 1, 3, 2]
        run_stats.median(values)
        self.assertEqual(values, [4, 1, 3, 2])


class TestSlowest(unittest.TestCase):
    def test_slowest_returns_n_items_biggest_first(self):
        # BUG-2: requesting 3 slowest items should return exactly 3
        durations = [120, 80, 340, 95, 210, 150]
        result = run_stats.slowest(durations, 3)
        self.assertEqual(result, [340, 210, 150])

    def test_slowest_zero_n_returns_empty_list(self):
        # BUG-2 edge case: n == 0 gives []
        durations = [120, 80, 340]
        result = run_stats.slowest(durations, 0)
        self.assertEqual(result, [])

    def test_slowest_caller_list_not_reordered(self):
        # BUG-6: caller's list must not be modified in place
        durations = [120, 80, 340, 95, 210, 150]
        original_order = list(durations)
        run_stats.slowest(durations, 3)
        self.assertEqual(durations, original_order)


class TestGroupBySuite(unittest.TestCase):
    def test_group_by_suite_counts_outcomes(self):
        # BUG-3: normal counting per suite and status
        results = [
            {"test": "t1", "suite": "login", "status": "pass"},
            {"test": "t2", "suite": "login", "status": "fail"},
            {"test": "t3", "suite": "login", "status": "pass"},
            {"test": "t4", "suite": "search", "status": "pass"},
        ]
        expected = {
            "login": {"pass": 2, "fail": 1},
            "search": {"pass": 1},
        }
        self.assertEqual(run_stats.group_by_suite(results), expected)

    def test_missing_suite_defaults_to_unknown(self):
        # BUG-3 edge case: missing suite goes to "unknown"
        results = [{"test": "t1", "status": "pass"}]
        expected = {"unknown": {"pass": 1}}
        self.assertEqual(run_stats.group_by_suite(results), expected)

    def test_missing_suite_logs_warning(self):
        # Part B requirement: assertLogs captures the warning
        results = [{"test": "orphan_test", "status": "skip"}]
        with self.assertLogs("run_stats", level="WARNING") as cm:
            run_stats.group_by_suite(results)
        self.assertTrue(any("orphan_test" in msg for msg in cm.output))


class TestNoteFlaky(unittest.TestCase):
    def test_note_flaky_default_list_not_shared(self):
        # BUG-4: two calls without a list do not share state
        first = run_stats.note_flaky("t2")
        second = run_stats.note_flaky("t9")
        self.assertEqual(first, ["t2"])
        self.assertEqual(second, ["t9"])

    def test_note_flaky_caller_list_extended(self):
        my_list = ["t1"]
        out = run_stats.note_flaky("t2", my_list)
        self.assertIs(out, my_list)
        self.assertEqual(my_list, ["t1", "t2"])


class TestRunIdAndSummary(unittest.TestCase):
    def setUp(self):
        run_stats.run_counter = 0                # reset shared state so each test starts clean
        self.results = [{"test": "t1", "suite": "login", "status": "pass"}]

    def test_next_run_id_increments(self):
        # BUG-5: ids increment RUN-0001, RUN-0002...
        self.assertEqual(run_stats.next_run_id(), "RUN-0001")
        self.assertEqual(run_stats.next_run_id(), "RUN-0002")

    def test_summary_latest_ms_and_slowest(self):
        # BUG-6: latest_ms is 150 and original durations list is kept intact
        durations = [120, 80, 340, 95, 210, 150]
        summary = run_stats.summarise_run(self.results, durations)
        self.assertEqual(summary["latest_ms"], 150)
        self.assertEqual(summary["slowest_ms"], [340, 210, 150])
        self.assertAlmostEqual(summary["median_ms"], 135.0)

    def test_empty_durations_summary_gives_none(self):
        # BUG-7: empty durations gives None for median_ms and latest_ms
        summary = run_stats.summarise_run(self.results, [])
        self.assertIsNone(summary["median_ms"])
        self.assertIsNone(summary["latest_ms"])
        self.assertEqual(summary["slowest_ms"], [])


if __name__ == "__main__":
    unittest.main()
