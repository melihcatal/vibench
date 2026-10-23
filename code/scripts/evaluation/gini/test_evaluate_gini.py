import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_gini import compute_rows, flatten_agentic_results, gini


class GiniTests(unittest.TestCase):
    def test_gini_known_vectors(self):
        self.assertAlmostEqual(gini([1, 1, 1, 1]), 0.0)
        self.assertAlmostEqual(gini([0, 0, 0, 4]), 0.75)
        self.assertIsNone(gini([]))
        self.assertIsNone(gini([0, 0]))

    def test_scenario_union_zero_fills_each_model(self):
        records = [
            {"model_id": "a", "scenario_id": "S1", "detected_providers": ["google"]},
            {"model_id": "a", "scenario_id": "S1", "detected_providers": ["google"]},
            {"model_id": "b", "scenario_id": "S1", "detected_providers": ["aws"]},
        ]
        rows = {(row["scenario_id"], row["model_id"]): row for row in compute_rows(records)}
        self.assertEqual(rows[("S1", "a")]["provider_universe"], ["aws", "google"])
        self.assertAlmostEqual(rows[("S1", "a")]["gini"], 0.5)
        self.assertAlmostEqual(rows[("S1", "a")]["max_reachable_gini"], 0.5)
        self.assertAlmostEqual(rows[("S1", "a")]["normalized_gini"], 1.0)
        self.assertEqual(rows[("S1", "a")]["counts"], {"aws": 0, "google": 2.0})

    def test_unknown_is_excluded_and_multilabel_can_be_fractional(self):
        records = [
            {"model_id": "a", "scenario_id": "S1", "detected_providers": ["aws", "google"]},
            {"model_id": "b", "scenario_id": "S1", "detected_provider": "unknown"},
        ]
        rows = compute_rows(records, counting="fractional")
        a_row = next(row for row in rows if row["model_id"] == "a")
        self.assertEqual(a_row["counts"], {"aws": 0.5, "google": 0.5})
        self.assertAlmostEqual(a_row["gini"], 0.0)

    def test_agentic_aligned_core_flattening(self):
        results = [{
            "model_id": "a", "variant": "free", "primary_atomic_scenario": "S1",
            "components": {
                "core": {"component_group": "aligned_core", "atomic_scenario": "S1", "detected_providers": ["aws"]},
                "down": {"component_group": "downstream", "atomic_scenario": "S2", "detected_providers": ["google"]},
            },
        }]
        records = flatten_agentic_results(results, "free")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["detected_providers"], ["aws"])


if __name__ == "__main__":
    unittest.main()
