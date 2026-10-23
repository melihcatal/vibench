import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'scripts/continue.py'
spec = importlib.util.spec_from_file_location('a1_continue', MODULE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.migration = self.root / 'migration.json'
        self.migration.write_text('{}')
        self.task = {'components': []}
        self.cell = {'scenario': 'S01', 'model': 'gemini-2.5-flash',
                     'condition': 'anchor_google', 'repetition': 1,
                     'task_sha256': runner.sha(runner.encoded(self.task)),
                     'prompt_sha256': runner.sha('prompt'),
                     'system_sha256': runner.sha('system'), 'seed_sha256': None}
        self.old = {'ablation': '1', 'timeout': 1200, 'sampling': {'variant': None},
                    'cells': [self.cell], 'code_sha256': {}}
        self.target = {**self.old, 'sampling': {'variant': None}}
        (self.root / 'runtime.json').write_text('{}')
        self.start(patch.object(runner, 'MIGRATION', self.migration))
        self.start(patch.object(runner.runtime.agentic, 'load_models', side_effect=lambda m: [{'id': m}]))
        self.start(patch.object(runner, 'effective_sampling', side_effect=lambda m,s: {'opencode_variant_sent_to_opencode': s['variant']}))

    def start(self, mock):
        self.addCleanup(mock.stop)
        return mock.start()

    def save_plan(self):
        (self.root / 'plan.json').write_text(json.dumps(self.old))

    def attempt(self, state='completed'):
        path = self.root / 'runs' / runner.cell_key(self.cell) / 'attempt_001'
        path.mkdir(parents=True)
        for name, value in [('input.json', {'cell': self.cell, 'task': self.task, 'model': {'id': self.cell['model']}}),
                            ('status.json', {'state': state}), ('response.json', {})]:
            (path / name).write_text(json.dumps(value))
        (path / 'prompt.txt').write_text('prompt')
        (path / 'system_prompt.txt').write_text('system')
        return path

    def plan(self):
        self.save_plan()
        return runner.continuation_plan(self.target, self.root)

    def test_retains_completed(self):
        self.attempt()
        result = self.plan()
        self.assertEqual(result['cells'], [])
        self.assertEqual(len(result['retained_attempts']), 1)

    def test_retains_failed_without_retry(self):
        self.attempt('failed')
        result = self.plan()
        self.assertEqual(result['cells'], [])
        self.assertEqual(result['retained_attempts'][0]['state'], 'failed')

    def test_schedules_unattempted(self):
        self.assertEqual(self.plan()['cells'], [self.cell])

    def test_excludes_old_gpt_and_schedules_corrected(self):
        self.cell['model'] = 'gpt-5.4-mini'
        self.target['sampling'] = {'variant': 'none'}
        self.attempt()
        result = self.plan()
        self.assertEqual(result['cells'], [self.cell])
        self.assertEqual(len(result['incompatible_archived_attempts']), 1)
        self.assertEqual(result['retained_attempts'], [])

    def test_rejects_undocumented_sampling_change(self):
        self.target['sampling'] = {'variant': 'high'}
        with self.assertRaisesRegex(ValueError, 'Unreviewed sampling'):
            self.plan()

    def test_rejects_modified_saved_prompt(self):
        path = self.attempt()
        (path / 'prompt.txt').write_text('modified')
        with self.assertRaisesRegex(ValueError, 'prompt mismatch'):
            self.plan()

    def test_rejects_nonterminal(self):
        self.attempt('running')
        with self.assertRaisesRegex(ValueError, 'Nonterminal'):
            self.plan()

    def test_rejects_unreviewed_source(self):
        source = self.root / 'source.py'
        source.write_text('changed')
        self.old['code_sha256'] = {str(source): 'oldhash'}
        with self.assertRaisesRegex(ValueError, 'Unreviewed source'):
            self.plan()

    def test_resume_skips_terminal_and_failed_local_attempts(self):
        path = self.attempt('failed')
        pending, skipped = runner.pending_cells(self.target, self.root, True, False)
        self.assertEqual(pending, [])
        self.assertEqual(skipped, 1)
        self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()
