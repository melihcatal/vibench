"""Execution-layer tests with no provider calls or OpenCode launches."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ablations.initial_provider.assigned_as_code.scripts import run as anchor
from ablations.agentic_mechanism.single_shot_multifile.scripts import run as multi_file, single_shot
from ablations.shared import (
    attempts, build_diffs, campaign, common, opencode, runtime, scoring, summarize, traces,
)


class RunnerTests(unittest.TestCase):
    def test_nova_first_party_routes(self):
        env = {
            'AMAZON_NOVA_API_KEY': 'test-only',
            'AMAZON_NOVA_API_BASE': 'https://api.nova.amazon.com/v1',
        }
        with patch.dict('os.environ', env, clear=True):
            for model_id, api_id in [('nova-pro', 'nova-pro-v1'), ('nova-2-lite', 'nova-2-lite-v1')]:
                with self.subTest(model=model_id):
                    model = runtime.agentic.load_models(model_id)[0]
                    self.assertEqual(model['litellm_string'], 'amazon_nova/' + api_id)
                    self.assertEqual(set(runtime.agentic.required_env_vars_for_model(model)), set(env))
                    runtime.agentic.validate_model_env([model], 'unused.env')
                    self.assertEqual(runtime.agentic.resolve_opencode_model(model_id)[0], 'amazon-nova-api/' + api_id)
                    config = runtime.agentic.build_workspace_provider_config(model_id)
                    provider = config['provider']['amazon-nova-api']
                    self.assertEqual(provider['options']['baseURL'], env['AMAZON_NOVA_API_BASE'])
                    self.assertEqual(provider['options']['apiKey'], '{env:AMAZON_NOVA_API_KEY}')
                    self.assertTrue(provider['models'][api_id]['tool_call'])

    def test_exported_diffs_match_both_ablations(self):
        files = build_diffs.desired_diffs()
        self.assertEqual(len(files), 80)
        self.assertFalse(list((common.HERE / 'diffs').glob('*.diff')))
        for name, content in files.items():
            with self.subTest(path=name):
                self.assertEqual((common.HERE / name).read_text(), content)

    def plan(self, ablation='1', extra=()):
        entry = anchor if ablation == '1' else multi_file
        args = entry.parser().parse_args(list(extra))
        return campaign.make_plan(args, entry.CONDITIONS, entry.cell_inputs)

    def execute_cell(self, plan, cell, attempt, database):
        entry = anchor if plan['ablation'] == '1' else multi_file
        data = entry.cell_inputs(cell['condition'], cell['scenario'], cell['model'])
        generate = opencode.generate if plan['ablation'] == '1' else multi_file.generate
        return attempts.execute_cell(plan, cell, attempt, database, data, generate)

    def test_plans_are_reproducible_and_balanced(self):
        for ablation, count in [('1', 1200), ('2', 120)]:
            plan = self.plan(ablation)
            self.assertEqual(plan, self.plan(ablation))
            self.assertEqual(len(plan['cells']), count)
            self.assertEqual({c['repetition'] for c in plan['cells']}, {1, 2, 3, 4, 5})
            self.assertEqual(len({attempts.cell_key(c) for c in plan['cells']}), count)
        with self.assertRaises(ValueError):
            self.plan(extra=['--models', 'typo'])

    def test_single_shot_targeted_scope_and_timeout(self):
        plan = self.plan('2')
        self.assertEqual(plan['timeout'], 300)
        self.assertEqual({c['model'] for c in plan['cells']},
                         {'gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini'})
        self.assertEqual({c['scenario'] for c in plan['cells']},
                         {'S03', 'S04', 'S07', 'S10', 'S14', 'S16', 'S18', 'S20'})
        self.assertEqual({c['condition'] for c in plan['cells']}, {'single_shot'})

    def test_original_and_anchored_prompts_unchanged(self):
        for sid in common.SCENARIOS:
            cell = anchor.cell_inputs('anchor_google', sid, 'nova-pro')
            original = (common.HERE / 'paper_inputs' / sid / 'original_prompt.txt').read_text()
            notice = f"The initial file {cell['seed_file']} is already implemented. Read it before generating the remaining files, and leave it unchanged.\n"
            self.assertEqual(cell['prompt'].replace(notice, '', 1), original)
            self.assertEqual(multi_file.cell_inputs('agentic', sid, 'nova-pro')['prompt'], original)
            single = multi_file.cell_inputs('single_shot', sid, 'nova-pro')
            restored_user = multi_file.replace_delivery(single['prompt'], {v: k for k, v in multi_file.SINGLE_SHOT_USER_REPLACEMENTS.items()})
            restored_system = multi_file.replace_delivery(single['system'], {v: k for k, v in multi_file.SINGLE_SHOT_SYSTEM_REPLACEMENTS.items()})
            self.assertEqual(restored_user, original)
            self.assertEqual(restored_system, (common.HERE / 'paper_inputs' / sid / 'opencode_agent_prompt.txt').read_text())
            self.assertNotIn('current working directory', single['prompt'] + single['system'])
            self.assertNotIn('Delivery for this single-response run:', single['prompt'])

    def test_dry_run_never_executes(self):
        with patch.object(campaign, 'preflight') as preflight, patch.object(campaign, 'execute_cell') as execute, redirect_stdout(io.StringIO()):
            anchor.main([])
            multi_file.main([])
            preflight.assert_not_called()
            execute.assert_not_called()

    def test_strict_json_transport(self):
        self.assertEqual(single_shot.parse_single_shot('{"a.py":"x = 1"}', ['a.py']), {'a.py': 'x = 1'})
        for text in ('{"../secret":"x"}', '{"a.py":1}', '[]', '{"a.py":"x","a.py":"y"}', 'Explanation\n```json\n{}\n```', '```json\n{}\n```\nExplanation'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                single_shot.parse_single_shot(text, ['a.py'])

    def test_single_json_fence(self):
        for opening in ('```json', '```'):
            text = opening + '\n{"a.py":"x = 1"}\n```'
            self.assertEqual(single_shot.parse_single_shot(text, ['a.py']), {'a.py': 'x = 1'})
        for text in ('```json\n{"a.py":"x","a.py":"y"}\n```', '```json\n{}\n```\n```json\n{}\n```'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                single_shot.parse_single_shot(text, ['a.py'])

    def test_attempts_preserve_failed_and_completed_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cell = Path(tmp) / 'cell'
            first = attempts.next_attempt(cell)
            common.write_json(first / 'status.json', {'state': 'failed'})
            with self.assertRaises(ValueError):
                attempts.next_attempt(cell)
            self.assertIsNone(attempts.next_attempt(cell, resume=True))
            second = attempts.next_attempt(cell, resume=True, retry_failed=True)
            self.assertEqual(second.name, 'attempt_002')
            common.write_json(second / 'status.json', {'state': 'completed'})
            self.assertIsNone(attempts.next_attempt(cell, resume=True, retry_failed=True))
            self.assertEqual(json.loads((first / 'status.json').read_text())['state'], 'failed')

    def test_trace_export_excludes_other_workspaces_and_includes_children(self):
        with tempfile.TemporaryDirectory() as tmp:
            dbpath = Path(tmp) / 'opencode.db'
            with sqlite3.connect(dbpath) as db:
                db.executescript('CREATE TABLE session (id TEXT, directory TEXT, parent_id TEXT);'
                                 'CREATE TABLE message (id TEXT, session_id TEXT, data TEXT);'
                                 'CREATE TABLE part (id TEXT, session_id TEXT, message_id TEXT, data TEXT);')
                db.executemany('INSERT INTO session VALUES (?,?,?)', [('root', '/chosen', None), ('child', '/elsewhere', 'root'), ('other', '/other', None)])
                db.executemany('INSERT INTO message VALUES (?,?,?)', [('m', 'root', '{}'), ('n', 'other', '{}')])
                db.execute('INSERT INTO part VALUES (?,?,?,?)', ('p', 'child', 'm', '{"type":"tool"}'))
            trace = traces.export_trace(dbpath, Path('/chosen'))
            self.assertEqual({s['id'] for s in trace['sessions']}, {'root', 'child'})
            self.assertEqual([m['id'] for m in trace['messages']], ['m'])
            self.assertEqual(len(trace['parts']), 1)

    def test_anchor_read_requires_a_later_assistant_turn(self):
        trace = {'messages': [{'id': 'read', 'data': {'time': {'created': 1}}},
                              {'id': 'write', 'data': {'time': {'created': 4}}}],
                 'parts': [{'message_id': 'read', 'data': {'type': 'tool', 'tool': 'read',
                            'state': {'status': 'completed', 'input': {'filePath': 'a.py'}, 'time': {'end': 3}}}},
                           {'message_id': 'write', 'data': {'type': 'tool', 'tool': 'write',
                            'state': {'status': 'completed', 'input': {'filePath': 'b.py'}, 'time': {'end': 6}}}}]}
        audit = traces.audit_anchor(trace, Path('/workspace'), 'a.py', 'seed', 'seed')
        self.assertTrue(audit['read_before_generation_verified'])
        trace['messages'][1]['data']['time']['created'] = 1
        self.assertFalse(traces.audit_anchor(trace, Path('/workspace'), 'a.py', 'seed', 'seed')['read_before_generation_verified'])
        trace['parts'].append({'message_id': 'write', 'data': {'type': 'tool', 'tool': 'bash'}})
        audit = traces.audit_anchor(trace, Path('/workspace'), 'a.py', 'seed', 'changed')
        self.assertIsNone(audit['read_before_generation_verified'])
        self.assertFalse(audit['final_hash_matches'])

    def test_scores_exclude_seed_and_retain_missing_denominator(self):
        data = anchor.cell_inputs('anchor_aws', 'S04', 'nova-pro')
        task = data['task']
        downstream = task['downstream_files'][0]
        scores = scoring.score_files(task, {data['seed_file']: data['seed'], downstream: 'import boto3\n'})
        self.assertEqual(scores['groups']['explicit']['aligned_core']['expected'], 3)
        group = scores['groups']['explicit']['downstream']
        self.assertEqual(group['expected'], 4)
        self.assertEqual(group['provider_share_all_expected']['aws'], .25)
        self.assertEqual(group['missing_or_unknown'], 3)

    def test_redaction(self):
        with patch.dict(common.os.environ, {'TEST_API_KEY': 'private-long-token'}):
            value = common.redact({'apiKey': 'other', 'stdout': 'token=private-long-token', 'nested': [{'x': 'private-long-token'}]})
        self.assertNotIn('private-long-token', json.dumps(value))
        self.assertEqual(value['apiKey'], '[REDACTED]')

    def test_mocked_agentic_run_reuses_original_runner_and_keeps_clean_input(self):
        plan = self.plan(extra=['--scenarios', 'S04', '--models', 'nova-pro', '--conditions', 'anchor_aws', '--repetitions', '1'])
        cell = plan['cells'][0]
        captured = {}
        def fake(task, prompt, workspace, model, **kwargs):
            self.assertEqual(list(workspace.iterdir()), [])
            captured['workspace'] = workspace
            self.assertEqual(prompt, anchor.cell_inputs('anchor_aws', 'S04', 'nova-pro')['prompt'])
            runtime.agentic.prepare_opencode_workspace(workspace, model, 'test/nova', kwargs['system_prompt'], kwargs['sampling'])
            runtime.agentic._materialize_seed_files(workspace, task)
            self.assertFalse((workspace / 'metadata.json').exists())
            for name in task['expected_files']:
                if not (workspace / name).exists():
                    (workspace / name).write_text('import boto3\n')
            return {'error': None, 'stdout': 'complete stdout', 'stderr': ''}
        with tempfile.TemporaryDirectory() as tmp, patch.object(runtime.agentic, 'run_opencode', side_effect=fake), patch.object(opencode, 'export_trace', return_value={'sessions': [{'id': 's'}], 'messages': [], 'parts': []}):
            attempt = Path(tmp)
            status = self.execute_cell(plan, cell, attempt, Path('/unused'))
            self.assertEqual(status['state'], 'completed')
            self.assertEqual(len(list((attempt / 'repository').glob('*.py'))), 10)
            audit = json.loads((attempt / 'anchor_audit.json').read_text())
            self.assertTrue(audit['final_hash_matches'])
            self.assertIsNone(audit['read_before_generation_verified'])
            self.assertFalse(captured['workspace'].exists())
            self.assertTrue((attempt / 'opencode.json').exists())
            self.assertTrue((attempt / 'trace.json').exists())

    def test_single_shot_keeps_raw_invalid_response(self):
        plan = self.plan('2', ['--scenarios', 'S04', '--models', 'nova-pro', '--conditions', 'single_shot', '--repetitions', '1'])
        with tempfile.TemporaryDirectory() as tmp, patch.object(single_shot, 'run_single_shot', return_value={'error': None, 'output_text': 'bad json'}):
            status = self.execute_cell(plan, plan['cells'][0], Path(tmp), Path('/unused'))
            self.assertEqual(status['state'], 'failed')
            self.assertEqual(json.loads((Path(tmp) / 'response.json').read_text())['output_text'], 'bad json')

    def test_single_shot_saves_all_files_without_opencode(self):
        plan = self.plan('2', ['--scenarios', 'S04', '--models', 'nova-pro', '--conditions', 'single_shot', '--repetitions', '1'])
        task = multi_file.cell_inputs('single_shot', 'S04', 'nova-pro')['task']
        response = {'error': None, 'output_text': json.dumps({name: 'import boto3\n' for name in task['expected_files']}), 'usage': {'total_tokens': 123}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(single_shot, 'run_single_shot', return_value=response), patch.object(runtime.agentic, 'run_opencode') as opencode:
            status = self.execute_cell(plan, plan['cells'][0], Path(tmp), Path('/unused'))
            self.assertEqual(status['state'], 'completed')
            self.assertEqual(len(list((Path(tmp) / 'repository').glob('*.py'))), 10)
            opencode.assert_not_called()

    def test_changed_input_fails_before_call(self):
        plan = self.plan('2', ['--scenarios', 'S04', '--models', 'nova-pro', '--conditions', 'single_shot', '--repetitions', '1'])
        plan['cells'][0]['prompt_sha256'] = 'changed'
        with tempfile.TemporaryDirectory() as tmp, patch.object(single_shot, 'run_single_shot') as model_call:
            with self.assertRaisesRegex(ValueError, 'Inputs changed'):
                self.execute_cell(plan, plan['cells'][0], Path(tmp), Path('/unused'))
            model_call.assert_not_called()

    def test_inventory_does_not_select_successful_retry(self):
        plan = self.plan('2', ['--scenarios', 'S04', '--models', 'nova-pro', '--conditions', 'single_shot', '--repetitions', '1'])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common.write_json(root / 'plan.json', plan)
            cell = root / 'runs' / attempts.cell_key(plan['cells'][0])
            first = attempts.next_attempt(cell)
            common.write_json(first / 'status.json', {'state': 'failed'})
            second = attempts.next_attempt(cell, resume=True, retry_failed=True)
            common.write_json(second / 'status.json', {'state': 'completed'})
            text = summarize.summarize(root)
            self.assertIn('| single_shot | nova-pro | 1 | 1 | 0 | 1 | 0 | 1 | 0 |', text)

    def test_s11_migration_required_before_runtime_or_model_calls(self):
        args = anchor.parser().parse_args(['--scenarios', 'S11', '--models', 'nova-pro', '--conditions', 'anchor_google'])
        plan = campaign.make_plan(args, anchor.CONDITIONS, anchor.cell_inputs)
        anchor.validate(plan, args)
        with patch.object(runtime, 'runtime_record') as runtime_check, patch.object(anchor, 'cell_inputs', return_value={'seed': 'import vertexai.generative_models'}), self.assertRaisesRegex(ValueError, 'Vertex-mode'):
            anchor.validate(plan, args)
        runtime_check.assert_not_called()

    def test_runners_reject_the_other_experiments_conditions(self):
        for entry, condition in [(anchor, 'single_shot'), (multi_file, 'anchor_aws')]:
            args = entry.parser().parse_args(['--conditions', condition])
            with self.assertRaises(ValueError):
                campaign.make_plan(args, entry.CONDITIONS, entry.cell_inputs)

    def test_retired_routes_block_before_credentials_or_calls(self):
        args = multi_file.parser().parse_args([])
        with patch.object(runtime.agentic, 'load_dotenv') as credentials:
            for model in ('deepseek-v3.2', 'grok-4-1-fast-reasoning'):
                with self.subTest(model=model), self.assertRaisesRegex(ValueError, 'retired model routes'):
                    runtime.preflight({'cells': [{'model': model}]}, args, True)
            credentials.assert_not_called()
        runtime.validate_model_routes({'cells': [{'model': 'gemini-2.5-flash'}, {'model': 'nova-pro'}]})


if __name__ == '__main__':
    unittest.main()
