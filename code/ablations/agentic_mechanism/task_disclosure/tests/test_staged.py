"""Offline protocol, session, failure, and audit tests; never call model APIs."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.agentic_mechanism.task_disclosure.scripts import run, staged, audit
from ablations.agentic_mechanism.task_disclosure.scripts.build_inputs import catalog, single_file_agent_prompt
from ablations.shared import campaign


class PromptTests(unittest.TestCase):
    def test_all_scenarios_match_and_never_disclose_future_specs_early(self):
        for sid in run.configuration()['scenarios']:
            full = run.cell_inputs('full_disclosure', sid, 'gemini-2.5-flash')
            hidden = run.cell_inputs('staged_disclosure', sid, 'gemini-2.5-flash')
            self.assertEqual([p.removeprefix(catalog(full['task'])) for p in full['prompts']], hidden['prompts'])
            self.assertEqual(full['system'], hidden['system'])
            self.assertEqual(len(hidden['prompts']), 10)
            self.assertEqual(hidden['task']['expected_files'][0], hidden['task']['primary_component_file'])
            for text in [hidden['system'], single_file_agent_prompt(hidden['system']), *hidden['prompts']]:
                for marker in ('multi-file', 'ten steps', 'Step ', 'SAME-SCENARIO', 'LATER-STEP', '[HELPER]'):
                    self.assertNotIn(marker, text)
            for i, name in enumerate(hidden['task']['expected_files']):
                self.assertIn(name, full['prompts'][0])
                for earlier in hidden['prompts'][:i]:
                    self.assertNotIn(name, earlier)
                self.assertIn(name, hidden['prompts'][i])
                component = next(c for c in hidden['task']['components'] if c['file'] == name)
                self.assertIn(component['description'], hidden['prompts'][i])

    def test_prompt_bundle_is_hashed_and_full_plan_scope(self):
        args = run.parser().parse_args([])
        plan = campaign.make_plan(args, tuple(run.configuration()['conditions']), run.cell_inputs)
        self.assertEqual(len(plan['cells']), 180)
        self.assertEqual({c['model'] for c in plan['cells']}, {'gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini'})
        self.assertEqual({c['scenario'] for c in plan['cells']}, {'S03', 'S04', 'S10', 'S14', 'S16', 'S20'})
        self.assertEqual({c['repetition'] for c in plan['cells']}, {1, 2, 3, 4, 5})
        self.assertEqual(plan['sampling']['opencode_variant_by_model']['gpt-5.4-mini'], 'none')
        self.assertIn('code/ablations/agentic_mechanism/task_disclosure/config.yaml', plan['code_sha256'])
        data = run.cell_inputs('full_disclosure', 'S04', 'nova-pro')
        self.assertEqual(json.loads(data['prompt']), data['prompts'])
        self.assertEqual(data['task']['seed_files'], [])

    def test_custom_yaml_and_cli_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'run.yaml'
            config.write_text('benchmark: vibench\ntype: agentic\nvariants: [free]\nmodels: [nova-pro]\ntasks: [S04]\nconditions: [staged_disclosure]\ncompletions: 2\ntimeout: 90\nmax_workers: 1\n')
            args = run.parse_args(['--config', str(config)])
            plan = campaign.make_plan(args, tuple(run.configuration()['conditions']), run.cell_inputs)
            self.assertEqual(len(plan['cells']), 2)
            self.assertEqual(plan['timeout'], 90)
            self.assertIn(str(config.resolve()), plan['code_sha256'])
            args = run.parse_args(['--config', str(config), '--models', 'gemini-2.5-flash', '--scenarios', 'S03', '--repetitions', '1'])
            plan = campaign.make_plan(args, tuple(run.configuration()['conditions']), run.cell_inputs)
            self.assertEqual(len(plan['cells']), 1)
            self.assertEqual(plan['cells'][0]['model'], 'gemini-2.5-flash')
            self.assertEqual(plan['cells'][0]['scenario'], 'S03')

    def test_bad_yaml_scope_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'run.yaml'
            with self.assertRaises(ValueError):
                run.parse_args(['--config', str(config)])
            for extra in ['variants: [informed]', 'tasks: [S99]', 'completions: 0', 'models: []']:
                config.write_text('benchmark: vibench\ntype: agentic\nvariants: [free]\n' + extra + '\n')
                with self.subTest(extra=extra), self.assertRaises(ValueError):
                    run.parse_args(['--config', str(config)])

    def test_dry_run_has_no_execution(self):
        with patch.object(campaign, 'preflight') as preflight, patch.object(campaign, 'execute_cell') as execute, redirect_stdout(io.StringIO()):
            run.main(['--models', 'nova-pro', '--scenarios', 'S04', '--repetitions', '1', '--check'])
            preflight.assert_not_called()
            execute.assert_not_called()

    def test_input_tampering_is_rejected(self):
        original = Path.read_text
        def read(path, *args, **kwargs):
            content = original(path, *args, **kwargs)
            return content + 'changed' if path.name == 'prompt_08.txt' else content
        with patch.object(Path, 'read_text', read), self.assertRaises(ValueError):
            run.cell_inputs('staged_disclosure', 'S04', 'nova-pro')


class AuditTests(unittest.TestCase):
    def test_unfinished_or_opaque_mutations_are_uncertain(self):
        parts = [{'id': 'p1', 'message_id': 'm', 'data': {'type': 'tool', 'tool': 'bash', 'state': {}}},
                 {'id': 'p2', 'message_id': 'm', 'data': {'type': 'tool', 'tool': 'write', 'state': {'status': 'error'}}}]
        result = audit.event_order({'messages': [], 'parts': parts}, Path('/tmp'), {}, ['a.py'])
        self.assertEqual(len(result['uncertain_activity']), 2)
        self.assertEqual(result['events'], [])

    def test_revisions_early_files_and_local_dependencies(self):
        result = audit.step_audit({'a.py': 'import helper\n'},
            {'a.py': 'import boto3\n', 'b.py': 'import helper\n', 'future.py': 'x=1\n'},
            'b.py', ['future.py', 'helper.py'], [], ['a.py', 'b.py', 'future.py', 'helper.py'])
        self.assertEqual(result['revised'], ['a.py'])
        self.assertEqual(result['off_target_changes'], ['a.py', 'future.py'])
        self.assertEqual(result['future_files_present'], ['future.py'])
        self.assertEqual(result['missing_local_imports'], {'b.py': ['helper.py']})

    def test_fresh_session_and_exact_prompt_required(self):
        t = {'sessions': [{'id': 'root', 'parent_id': None}, {'id': 'child', 'parent_id': 'root'}],
             'messages': [{'id': 'u', 'session_id': 'root', 'data': {'role': 'user'}}],
             'parts': [{'message_id': 'u', 'data': {'type': 'text', 'text': 'current'}}]}
        self.assertEqual(staged.fresh_session(t, set(), 'current')[0], 'root')
        with self.assertRaises(RuntimeError):
            staged.fresh_session(t, {'root'}, 'current')
        with self.assertRaises(RuntimeError):
            staged.fresh_session(t, set(), 'different')
        t['messages'].append({'id': 'u2', 'session_id': 'root', 'data': {'role': 'user'}})
        with self.assertRaises(RuntimeError):
            staged.fresh_session(t, set(), 'current')

    def test_provider_errors_detected_even_with_zero_exit(self):
        trace = {'messages': [{'id': 'old', 'data': {'error': 'old error'}},
                              {'id': 'new', 'data': {'error': 'new error'}}]}
        errors = staged.response_errors('{"type":"error","error":"bad"}', trace, {'old'})
        self.assertEqual(len(errors), 2)

    def test_symlink_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'outside.txt').write_text('secret')
            (root / 'link.py').symlink_to(root / 'outside.txt')
            content, unsafe = audit.snapshot(root)
            self.assertNotIn('link.py', content)
            self.assertEqual(unsafe, ['link.py'])


class ConversationTests(unittest.TestCase):
    def test_server_failure_and_interruption_cleanup(self):
        for failure in (False, KeyboardInterrupt()):
            conversation = object.__new__(staged.Conversation)
            conversation.workspace, conversation.env = Path('/tmp'), {}
            process = Mock()
            with patch.object(staged.agentic, '_free_port', return_value=1), patch.object(staged.subprocess, 'Popen', return_value=process), patch.object(staged.agentic, '_wait_for_port', side_effect=failure if isinstance(failure, BaseException) else None, return_value=failure):
                with self.assertRaises(KeyboardInterrupt if isinstance(failure, BaseException) else RuntimeError):
                    conversation.__enter__()
                process.terminate.assert_called_once()
                process.wait.assert_called_once()

    def test_cli_never_resumes_an_earlier_conversation(self):
        conversation = object.__new__(staged.Conversation)
        conversation.workspace, conversation.route = Path('/tmp'), 'test/model'
        conversation.url, conversation.env, conversation.sampling = 'http://localhost:1', {}, {}
        with patch.object(staged.subprocess, 'run', return_value=Mock(returncode=0, stdout='', stderr='')) as call:
            conversation.send('first', 20)
            self.assertNotIn('--session', call.call_args.args[0])
            conversation.send('second', 15)
            command = call.call_args.args[0]
            self.assertNotIn('--session', command)
            self.assertNotIn('--continue', command)
            self.assertEqual(call.call_args.kwargs['timeout'], 15)

    def exercise(self, failure_step=None, revise=False, reuse_session=False):
        data = run.cell_inputs('staged_disclosure', 'S04', 'gemini-2.5-flash')
        names = data['task']['expected_files']
        holder = {}
        class FakeConversation:
            route, identity_mode, identity_note, sampling = 'test/model', 'test', None, {}
            def __init__(self, workspace, *_):
                self.workspace, self.index = workspace, 0
                self.messages, self.parts, self.sessions, self.timeouts = [], [], [], []
                holder['conversation'] = self
            def __enter__(self):
                return self
            def __exit__(self, *_):
                holder['closed'] = True
            def send(self, prompt, timeout):
                self.index += 1
                sid = 'session-1' if reuse_session else f'session-{self.index}'
                if sid not in [s['id'] for s in self.sessions]:
                    self.sessions.append({'id': sid, 'parent_id': None})
                self.timeouts.append(timeout)
                name, mid = names[self.index - 1], f'm{self.index}'
                (self.workspace / name).write_text('import boto3\n')
                if revise and self.index == 2:
                    (self.workspace / names[0]).write_text('from google.cloud import speech\n')
                self.messages.append({'id': f'u{self.index}', 'session_id': sid, 'data': {'role': 'user'}})
                self.parts.append({'id': f'up{self.index}', 'message_id': f'u{self.index}', 'data': {'type': 'text', 'text': prompt}})
                self.messages.append({'id': mid, 'session_id': sid, 'data': {'role': 'assistant', 'time': {'created': self.index * 100}}})
                self.parts.append({'id': f'p{self.index}', 'message_id': mid, 'data': {
                    'type': 'tool', 'tool': 'write', 'state': {'status': 'completed',
                    'input': {'filePath': str(self.workspace / name)},
                    'time': {'start': self.index * 100 + 1, 'end': self.index * 100 + 2}}}})
                if self.index == failure_step:
                    raise subprocess.TimeoutExpired('fake', timeout)
                return {'exit_code': 0, 'stdout': '', 'stderr': '', 'error': None}
        def trace(*_):
            c = holder['conversation']
            return {'sessions': c.sessions[:], 'messages': c.messages[:], 'parts': c.parts[:]}
        with tempfile.TemporaryDirectory() as tmp, patch.object(staged, 'Conversation', FakeConversation), patch.object(staged, 'export_trace', trace):
            out = {'response': {}, 'files': {}, 'audit': {}, 'errors': []}
            staged.generate(data, {}, {'timeout': 1200, 'sampling': {}}, Path(tmp), None, out)
            saved = json.loads((Path(tmp) / 'disclosure_audit.json').read_text())
            steps = sorted((Path(tmp) / 'steps').iterdir())
            self.assertTrue((steps[0] / 'repository' / names[0]).exists())
            self.assertTrue((Path(tmp) / 'trace.json').exists())
        self.assertTrue(holder['closed'])
        self.assertFalse(holder['conversation'].workspace.exists())
        return out, saved, holder['conversation']

    def test_ten_fresh_sessions_preserve_repository_not_prompts(self):
        out, saved, conversation = self.exercise()
        self.assertEqual(len(out['files']), 10)
        self.assertNotIn('error', out['response'])
        self.assertEqual(len(saved['root_session_ids']), 10)
        self.assertEqual(saved['steps_attempted'], 10)
        self.assertEqual(saved['snapshot_noncompliance_steps'], [])
        self.assertEqual(set(saved['primary_first_mutation_vs_downstream'].values()), {'sequential'})
        self.assertEqual(conversation.timeouts, sorted(conversation.timeouts, reverse=True))

    def test_timeout_keeps_partial_outputs_and_stops_later_steps(self):
        out, saved, _ = self.exercise(failure_step=3)
        self.assertEqual(len(out['files']), 3)
        self.assertIn('error', out['response'])
        self.assertEqual(saved['steps_attempted'], 3)

    def test_revisions_retained_and_flagged_not_discarded(self):
        out, saved, _ = self.exercise(revise=True)
        self.assertEqual(len(out['files']), 10)
        self.assertNotIn('error', out['response'])
        self.assertEqual(saved['snapshot_noncompliance_steps'], [2])

    def test_session_reuse_fails_instead_of_silent_history_carryover(self):
        out, saved, _ = self.exercise(reuse_session=True)
        self.assertIn('fresh root', out['response']['error'])
        self.assertEqual(saved['steps_attempted'], 2)


if __name__ == '__main__':
    unittest.main()
