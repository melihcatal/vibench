"""Offline safeguards for the explicit timeout migration."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ablations.shared import timeout_continuation as runner


class TimeoutContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.previous = self.root / 'previous'
        self.previous.mkdir()
        migration = self.root / 'migrations.json'
        migration.write_text('{}')
        self.task = {'components': []}
        self.cell = {'scenario': 'S01', 'model': 'nova-pro', 'condition': 'full_disclosure',
                     'repetition': 1, 'task_sha256': runner.sha(runner.encoded(self.task)),
                     'prompt_sha256': runner.sha('prompt'), 'system_sha256': runner.sha('system')}
        self.old = {'ablation': '4', 'timeout': 1200, 'sampling': {}, 'cells': [self.cell]}
        self.target = {**self.old, 'timeout': 300}
        self.start(patch.object(runner, 'MIGRATIONS', migration))
        self.start(patch.object(runner, 'verify_sources', side_effect=lambda root, migrations: runner.read_plan(root)))
        self.start(patch.object(runner.runtime.agentic, 'load_models', side_effect=lambda m: [{'id': m}]))
        self.start(patch.object(runner, 'effective_sampling', side_effect=lambda m,s: s))

    def start(self, obj):
        self.addCleanup(obj.stop)
        return obj.start()

    def save(self):
        (self.previous / 'plan.json').write_text(json.dumps(self.old))
        (self.previous / 'runtime.json').write_text('{}')

    def attempt(self, state):
        path = self.previous / 'runs' / runner.cell_key(self.cell) / 'attempt_001'
        path.mkdir(parents=True)
        (path / 'input.json').write_text(json.dumps({'cell': self.cell, 'task': self.task, 'model': {'id': 'nova-pro'}}))
        (path / 'status.json').write_text(json.dumps({'state': state, 'elapsed_seconds': 1200}))
        (path / 'prompt.txt').write_text('prompt')
        (path / 'system_prompt.txt').write_text('system')
        return path

    def plan(self):
        self.save()
        return runner.continuation_plan(self.target, self.previous)

    def test_pending_only_is_scheduled(self):
        result = self.plan()
        self.assertEqual(result['cells'], [self.cell])
        self.assertEqual(result['timeout'], 300)

    def test_completed_budget_not_relabeled(self):
        self.attempt('completed')
        result = self.plan()
        self.assertEqual(result['cells'], [])
        self.assertEqual(result['retained_attempts'][0]['timeout_seconds'], 1200)
        self.assertEqual(result['timeout_migration'], {'archived': 1200, 'new': 300})

    def test_failures_retained_without_retry(self):
        self.attempt('failed')
        result = self.plan()
        self.assertEqual(result['cells'], [])
        self.assertEqual(result['retained_attempts'][0]['state'], 'failed')

    def test_running_archive_rejected(self):
        self.attempt('running')
        with self.assertRaisesRegex(ValueError, 'nonterminal'):
            self.plan()

    def test_scope_change_rejected(self):
        self.target = {**self.target, 'cells': []}
        with self.assertRaisesRegex(ValueError, 'coverage mismatch'):
            self.plan()

    def test_sampling_change_rejected(self):
        self.target['sampling'] = {'variant': 'none'}
        with self.assertRaisesRegex(ValueError, 'Sampling changed'):
            self.plan()

    def test_inherited_attempt_preserved_once(self):
        path = self.attempt('completed')
        first = self.plan()['retained_attempts'][0]
        parent = self.previous
        self.previous = self.root / 'continuation'
        self.previous.mkdir()
        self.old = {**self.old, 'cells': [], 'retained_attempts': [first],
                    'previous_campaign': str(parent),
                    'previous_plan_sha256': runner.sha(runner.encoded(runner.read_plan(parent))),
                    'previous_runtime_sha256': runner.sha((parent / 'runtime.json').read_text())}
        result = self.plan()
        self.assertEqual(result['cells'], [])
        self.assertEqual(len(result['retained_attempts']), 1)
        self.assertEqual(result['retained_attempts'][0]['source_campaign'], str(parent))
        (path / 'status.json').write_text(json.dumps({'state': 'failed'}))
        with self.assertRaisesRegex(ValueError, 'Inherited attempt changed'):
            self.plan()


if __name__ == '__main__':
    unittest.main()
