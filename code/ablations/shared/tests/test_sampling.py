"""Offline checks of the actual original adapters' reasoning arguments."""
import json
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from ablations.shared import campaign, configuration, runtime
from ablations.shared.sampling_audit import audit_sampling
from ablations.initial_provider.assigned_as_code.scripts import run as a1
from ablations.agentic_mechanism.single_shot_multifile.scripts import run as a2
from ablations.initial_provider.by_instruction.scripts import run as a3
from ablations.agentic_mechanism.task_disclosure.scripts import run as a4, staged


class SamplingTests(unittest.TestCase):
    def test_all_yaml_defaults_inherit_both_original_policies(self):
        expected = configuration.paper_sampling()
        for entry in [a1, a2, a3, a4]:
            args = entry.parser().parse_args([])
            self.assertEqual(args.sampling, expected)
            self.assertEqual(args.repetitions, 5)
            self.assertEqual(args.timeout, 300)
            self.assertEqual(args.max_consecutive_errors, 5)
            for key in ['opencode_variant_by_model', 'reasoning_effort_by_model']:
                self.assertEqual(args.sampling[key]['gpt-5.4-mini'], 'none')
                self.assertEqual(args.sampling[key]['gpt-5.4'], 'none')

    def test_cli_rejects_timeouts_above_five_minutes(self):
        for entry in [a1, a2, a3, a4]:
            with self.subTest(ablation=entry.__name__), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    entry.parser().parse_args(['--timeout', '301'])
            self.assertEqual(entry.parser().parse_args(['--timeout', '60']).timeout, 60)

    def test_yaml_rejects_timeouts_above_five_minutes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'config.yaml'
            path.write_text('benchmark: vibench\ntype: agentic\nvariants: [free]\ncompletions: 5\ntimeout: 301\nmax_workers: 1\n')
            with self.assertRaisesRegex(ValueError, 'must not exceed 300'):
                configuration.run_settings(path, ['nova-pro'], ['S04'], ['anchor_google'])

    def test_direct_adapter_passes_none_only_for_gpt(self):
        import run_direct
        for model_id in ['gpt-5.4', 'gpt-5.4-mini', 'gemini-2.5-flash', 'nova-pro', 'qwen3.6-plus']:
            model = runtime.agentic.load_models(model_id)[0]
            with patch.object(run_direct.litellm, 'completion', side_effect=RuntimeError('offline test')) as call:
                run_direct.call_model(model, 'system', 'prompt', configuration.paper_sampling())
            kwargs = call.call_args.kwargs
            if model_id.startswith('gpt-'):
                self.assertEqual(kwargs['reasoning_effort'], 'none')
            else:
                self.assertNotIn('reasoning_effort', kwargs)
            for key in ['temperature', 'top_p', 'max_tokens']:
                self.assertNotIn(key, kwargs)

    def test_original_opencode_adapter_passes_none(self):
        agentic = runtime.agentic
        model = agentic.load_models('gpt-5.4-mini')[0]
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(agentic, '_free_port', return_value=9999), \
             patch.object(agentic, '_wait_for_port', return_value=True), \
             patch.object(agentic.subprocess, 'Popen', return_value=Mock()), \
             patch.object(agentic.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as call:
            result = agentic.run_opencode({}, 'prompt', Path(tmp), model,
                                          sampling=configuration.paper_sampling())
        cmd = call.call_args.args[0]
        self.assertEqual(cmd[cmd.index('--variant') + 1], 'none')
        self.assertEqual(result['sampling']['opencode_variant_sent_to_opencode'], 'none')

    def test_staged_adapter_passes_none_and_no_chat_continuation(self):
        model = runtime.agentic.load_models('gpt-5.4-mini')[0]
        data = a4.cell_inputs('staged_disclosure', 'S04', model['id'])
        with tempfile.TemporaryDirectory() as tmp:
            conversation = staged.Conversation(Path(tmp), model, data['system'], configuration.paper_sampling())
            conversation.url = 'http://127.0.0.1:9999'
            with patch.object(staged.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as call:
                conversation.send('prompt', 10)
            cmd = call.call_args.args[0]
            self.assertEqual(cmd[cmd.index('--variant') + 1], 'none')
            self.assertNotIn('--session', cmd)
            self.assertNotIn('--continue', cmd)

    def test_unsupported_reasoning_fails_before_execution(self):
        args = a1.parser().parse_args(['--models', 'gemini-2.5-flash', '--scenarios', 'S04'])
        args.sampling['opencode_variant_by_model']['gemini-2.5-flash'] = 'not-a-real-variant'
        plan = campaign.make_plan(args, a1.CONDITIONS, a1.cell_inputs)
        with self.assertRaisesRegex(ValueError, 'would be dropped'):
            runtime.validate_model_routes(plan)

    def test_usage_audit_warns_without_relabeling_observed_reasoning(self):
        model = runtime.agentic.load_models('gpt-5.4-mini')[0]
        with tempfile.TemporaryDirectory() as tmp:
            trace = Path(tmp) / 'trace.json'
            trace.write_text(json.dumps({'messages': [{'id': 'm', 'data': {'role': 'assistant', 'tokens': {'reasoning': 12}}}]}))
            audit = audit_sampling(model, configuration.paper_sampling(), {}, trace)
            self.assertEqual(audit['reasoning_tokens_reported'], 12)
            self.assertTrue(audit['warnings'])
            audit = audit_sampling(model, configuration.paper_sampling(), {}, Path(tmp) / 'missing.json')
            self.assertIsNone(audit['reasoning_tokens_reported'])
