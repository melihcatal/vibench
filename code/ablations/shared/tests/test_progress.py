"""Offline progress/concurrency and strict suite ordering checks."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Barrier, Lock
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ablations.shared import progress
from ablations.shared.common import ROOT


class FakeBar:
    def __init__(self, **kwargs):
        self.total, self.n = kwargs['total'], 0
    def update(self, n):
        self.n += n
    def set_postfix_str(self, text):
        pass
    def close(self):
        pass
    @staticmethod
    def write(text):
        pass


class ProgressTests(unittest.TestCase):
    def args(self, **overrides):
        values = dict(resume=False, retry_failed=False, limit=None, workers=2,
                      sequential=False, trace_db=None, max_consecutive_errors=3)
        return SimpleNamespace(**(values | overrides))

    def plan(self):
        return {'cells': [{'model': m, 'scenario': 'S04', 'condition': 'test', 'repetition': r}
                          for r in (1, 2) for m in ('a', 'b')]}

    def load(self, *args):
        return {'task': {'expected_files': ['a.py']}, 'seed_file': None}

    def run_jobs(self, root, execute, **overrides):
        with patch.object(progress, 'tqdm', FakeBar), redirect_stdout(io.StringIO()):
            return progress.run_jobs(self.plan(), self.args(**overrides), root, self.load, None, execute)

    def test_parallel_models_sequential_per_model(self):
        barrier, lock = Barrier(2), Lock()
        active, seen = set(), []
        def execute(plan, cell, attempt, database, data, generate):
            with lock:
                self.assertNotIn(cell['model'], active)
                active.add(cell['model'])
                seen.append((cell['model'], cell['repetition']))
            barrier.wait(timeout=3)
            with lock:
                active.remove(cell['model'])
            status = {'state': 'completed', 'missing_generated_files': []}
            (attempt / 'status.json').write_text(json.dumps(status))
            return status
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = self.run_jobs(root, execute)
            self.assertEqual(summary['completed'], 4)
            self.assertEqual(summary['workers'], 2)
            self.assertEqual([r for m, r in seen if m == 'a'], [1, 2])
            self.assertEqual([r for m, r in seen if m == 'b'], [1, 2])
            self.assertEqual(len(list((root / 'logs').glob('*.jsonl'))), 2)
            summary = self.run_jobs(root, execute, resume=True)
            self.assertEqual(summary['scheduled'], 0)
            self.assertEqual(summary['pre_skipped'], 4)

    def test_limit_is_global_not_per_worker(self):
        calls = []
        def execute(plan, cell, *args):
            calls.append(cell)
            return {'state': 'completed'}
        with tempfile.TemporaryDirectory() as tmp:
            summary = self.run_jobs(Path(tmp), execute, limit=1)
            self.assertEqual(len(calls), 1)
            self.assertEqual(summary['scheduled'], 1)

    def test_failures_remain_visible_on_resume(self):
        def execute(plan, cell, attempt, *args):
            status = {'state': 'failed', 'missing_generated_files': ['a.py']}
            (attempt / 'status.json').write_text(json.dumps(status))
            return status
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(RuntimeError):
                self.run_jobs(root, execute)
            with self.assertRaises(RuntimeError):
                self.run_jobs(root, execute, resume=True)
            self.assertEqual(json.loads((root / 'progress.json').read_text())['unresolved_previous_attempts'], 4)

    def test_sequential_override_and_per_model_fail_fast(self):
        seen = []
        def execute(plan, cell, *args):
            seen.append(cell['model'])
            return {'state': 'failed' if cell['model'] == 'a' else 'completed'}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(RuntimeError):
                self.run_jobs(root, execute, sequential=True, max_consecutive_errors=1)
            summary = json.loads((root / 'progress.json').read_text())
            self.assertEqual(summary['workers'], 1)
            self.assertEqual(seen, ['a', 'b', 'b'])
            self.assertEqual(set(summary['aborted_models']), {'a'})


class SuiteTests(unittest.TestCase):
    def suite(self, fail='', default_scope=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = root / 'fake-python'
            log = root / 'events.jsonl'
            helper.write_text('#!' + sys.executable + '\n' +
                'import json,os,sys,time\n' +
                'stage=next(x for x in sys.argv if "/ablation_" in x).split("/ablation_")[-1].split("/")[0]\n' +
                'mode="execute" if "--execute" in sys.argv else "check"\n' +
                'with open(os.environ["TEST_LOG"],"a") as f: f.write(json.dumps([stage,mode,"start",sys.argv])+"\\n")\n' +
                'time.sleep(0.01)\n' +
                'with open(os.environ["TEST_LOG"],"a") as f: f.write(json.dumps([stage,mode,"end"])+"\\n")\n' +
                'sys.exit(7 if mode=="execute" and stage==os.environ.get("FAIL_STAGE") else 0)\n')
            helper.chmod(0o700)
            flags = [] if default_scope else ['--models', 'gemini-2.5-flash,nova-pro']
            result = subprocess.run(['bash', str(ROOT / 'code/ablations/shared/scripts/run_sequential.sh'),
                                     str(root / 'out'), *flags, '--execute'],
                                    env=os.environ | {'PYTHON_BIN': str(helper), 'TEST_LOG': str(log), 'FAIL_STAGE': fail},
                                    capture_output=True, text=True, timeout=10)
            events = [json.loads(line) for line in log.read_text().splitlines()]
            return result, events

    def test_all_checks_then_strictly_sequential_ablations(self):
        result, events = self.suite()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([e[:3] for e in events], [[s, mode, event] for mode in ('check', 'execute') for s in ('1', '2', '3', '4') for event in ('start', 'end')])
        commands = [e[3] for e in events if e[2] == 'start']
        for command in commands:
            self.assertNotIn('--conditions', command)

    def test_default_scope_preserves_stage_yaml(self):
        result, events = self.suite(default_scope=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for event in events:
            if event[:3] == ['4', 'check', 'start']:
                self.assertNotIn('--models', event[3])
                self.assertNotIn('--scenarios', event[3])
                self.assertNotIn('--conditions', event[3])

    def test_failure_prevents_next_ablation(self):
        result, events = self.suite(fail='2')
        self.assertEqual(result.returncode, 7)
        self.assertNotIn(['3', 'execute', 'start'], [e[:3] for e in events])
        self.assertNotIn(['4', 'execute', 'start'], [e[:3] for e in events])


if __name__ == '__main__':
    unittest.main()
