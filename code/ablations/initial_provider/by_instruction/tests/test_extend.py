import copy
from pathlib import Path
import tempfile
import unittest

from ablations.initial_provider.by_instruction.scripts.extend import extension_plan
from ablations.shared.attempts import cell_key
from ablations.shared.common import write_json


class ExtensionTests(unittest.TestCase):
    def fixture(self, root):
        cells = [dict(model='m', scenario=s, condition=c, repetition=1,
                      prompt_sha256='p', system_sha256='s', seed_sha256=None, task_sha256='t')
                 for s in ('S03', 'S04') for c in ('instruct_google', 'instruct_aws')]
        target = dict(ablation='3', sampling={}, timeout=300, code_sha256={}, cells=cells)
        write_json(root / 'plan.json', {**target, 'cells': cells[:2]})
        for cell, state in zip(cells, ('completed', 'failed')):
            attempt = root / 'runs' / cell_key(cell) / 'attempt_001'
            attempt.mkdir(parents=True)
            write_json(attempt / 'status.json', {'state': state})
            write_json(attempt / 'input.json', {'cell': cell})
            write_json(attempt / 'response.json', {'stdout': 'raw'})
        return target

    def test_skip_both_terminal_states_and_keep_both_new_conditions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            plan = extension_plan(target, root)
            self.assertEqual(plan['cells'], target['cells'][2:])
            self.assertEqual([r['state'] for r in plan['retained_attempts']], ['completed', 'failed'])
            self.assertEqual(plan, extension_plan(target, root))

    def test_reject_different_budget_prompt_or_condition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            for key, value in [('timeout', 1200), ('sampling', {'temperature': 1})]:
                with self.subTest(key=key), self.assertRaises(ValueError):
                    extension_plan({**target, key: value}, root)
            for key, value in [('prompt_sha256', 'different'), ('condition', 'single_shot')]:
                changed = copy.deepcopy(target)
                changed['cells'][0][key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    extension_plan(changed, root)

    def test_running_attempt_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = self.fixture(root)
            write_json(root / 'runs' / cell_key(target['cells'][0]) / 'attempt_001/status.json',
                       {'state': 'running'})
            with self.assertRaises(ValueError):
                extension_plan(target, root)


if __name__ == '__main__':
    unittest.main()
