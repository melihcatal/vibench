import copy
import tempfile
import unittest
from pathlib import Path

from ablations.agentic_mechanism.single_shot_multifile.scripts.extend import extension_plan
from ablations.shared.attempts import cell_key
from ablations.shared.common import write_json


class ExtensionTests(unittest.TestCase):
    def fixture(self, root):
        cells = [dict(model='m', scenario='S03', condition='single_shot', repetition=i,
                      prompt_sha256='p', system_sha256='s', seed_sha256=None, task_sha256='t') for i in (1, 2, 3)]
        target = dict(ablation='2', sampling={}, timeout=300, code_sha256={}, cells=cells)
        old = {**target, 'cells': cells[:2]}
        write_json(root / 'plan.json', old)
        for cell, state in zip(cells, ('completed', 'failed')):
            attempt = root / 'runs' / cell_key(cell) / 'attempt_001'
            attempt.mkdir(parents=True)
            write_json(attempt / 'status.json', {'state': state})
            write_json(attempt / 'input.json', {'cell': cell})
            write_json(attempt / 'response.json', {'output_text': 'raw'})
        return target

    def test_completed_and_failed_attempts_are_retained_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            plan = extension_plan(target, root)
            self.assertEqual(plan['cells'], target['cells'][2:])
            self.assertEqual([r['state'] for r in plan['retained_attempts']], ['completed', 'failed'])
            self.assertEqual(plan['requested_cell_count'], 3)
            self.assertEqual(plan, extension_plan(target, root))

    def test_changed_sampling_budget_or_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            for key, value in [('timeout', 600), ('sampling', {'temperature': 1})]:
                with self.subTest(key=key), self.assertRaises(ValueError):
                    extension_plan({**target, key: value}, root)
            changed = copy.deepcopy(target)
            changed['cells'][0]['prompt_sha256'] = 'different'
            with self.assertRaises(ValueError):
                extension_plan(changed, root)

    def test_running_attempt_is_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            path = root / 'runs' / cell_key(target['cells'][0]) / 'attempt_001/status.json'
            write_json(path, {'state': 'running'})
            with self.assertRaises(ValueError):
                extension_plan(target, root)


if __name__ == '__main__':
    unittest.main()
