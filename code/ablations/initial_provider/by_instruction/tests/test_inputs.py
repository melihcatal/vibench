"""Offline checks for the instruction-only experiment."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.initial_provider.by_instruction.scripts import run, build_inputs
from ablations.shared import campaign


class InstructionTests(unittest.TestCase):
    def test_single_sentence_and_no_seed_for_every_cell(self):
        config = run.configuration()
        for sid in config['scenarios']:
            original = (run.BASE / 'sources' / sid / 'original_prompt.txt').read_text()
            for condition, provider in config['conditions'].items():
                for model in config['models']:
                    data = run.cell_inputs(condition, sid, model)
                    notice = build_inputs.instruction(data['task'], provider) + '\n'
                    self.assertEqual(data['prompt'].replace(notice, '', 1), original)
                    self.assertEqual(data['prompt'].count(notice), 1)
                    self.assertIsNone(data['seed'])
                    self.assertIsNone(data['seed_file'])
                    self.assertEqual(data['task']['seed_files'], [])
                    self.assertEqual(len(data['task']['expected_files']), 10)

    def test_scope_and_no_unassigned_condition(self):
        args = run.parser().parse_args([])
        plan = campaign.make_plan(args, tuple(run.configuration()['conditions']), run.cell_inputs)
        self.assertEqual(len(plan['cells']), 240)
        self.assertEqual(plan['timeout'], 300)
        self.assertEqual(args.workers, 3)
        self.assertEqual({c['model'] for c in plan['cells']},
                         {'gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini'})
        self.assertEqual({c['scenario'] for c in plan['cells']},
                         {'S03', 'S04', 'S07', 'S10', 'S14', 'S16', 'S18', 'S20'})
        self.assertEqual({c['repetition'] for c in plan['cells']}, {1, 2, 3, 4, 5})
        self.assertEqual({c['condition'] for c in plan['cells']}, {'instruct_google', 'instruct_aws'})
        with self.assertRaises(ValueError):
            campaign.make_plan(run.parser().parse_args(['--models', 'granite-4.0-h-small']), tuple(run.configuration()['conditions']), run.cell_inputs)

    def test_dry_run_never_calls_models(self):
        with patch.object(campaign, 'preflight') as preflight, patch.object(campaign, 'execute_cell') as execute, redirect_stdout(io.StringIO()):
            run.main(['--models', 'nova-pro', '--scenarios', 'S04', '--repetitions', '1'])
            preflight.assert_not_called()
            execute.assert_not_called()

    def test_compliance_is_recorded_not_used_to_discard(self):
        data = run.cell_inputs('instruct_aws', 'S04', 'nova-pro')
        initial = data['task']['primary_component_file']
        outcome = {'files': {initial: 'from google.cloud import speech\n'}, 'errors': []}
        with tempfile.TemporaryDirectory() as tmp, patch.object(run.opencode, 'generate'):
            run.generate(data, {}, {}, Path(tmp), None, outcome)
            audit = json.loads((Path(tmp) / 'assignment_audit.json').read_text())
            self.assertFalse(audit['explicit']['includes_assigned'])
            self.assertEqual(outcome['errors'], [])


if __name__ == '__main__':
    unittest.main()
