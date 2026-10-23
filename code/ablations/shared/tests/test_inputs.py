"""Offline checks only: no model calls, SDK installation, or cloud requests."""
import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ablations.initial_provider.assigned_as_code.scripts import build_inputs as build

sys.path.insert(0, str(build.ROOT / 'code/scripts/evaluation/core'))
from evaluate_agentic import detect_provider_from_file


class InputTests(unittest.TestCase):
    def test_materialized_tree_matches_sources(self):
        desired = build.desired_files()
        for name, content in desired.items():
            with self.subTest(path=name):
                self.assertEqual((build.HERE / name).read_text(), content)
        manifest = json.loads((build.HERE / 'initial_provider/assigned_as_code/manifest.json').read_text())
        self.assertEqual(len(manifest['cells']), 240)
        self.assertEqual(sum(len(list((build.HERE / c['path'] / 'workspace').glob('*.py'))) for c in manifest['cells']), 240)
        self.assertEqual(sum(len(list((build.HERE / c['path'] / 'workspace').glob('a1.py')))
                             for c in manifest['cells']), 0)
        self.assertEqual(sum((build.HERE / c['path'] / 'prompt.txt').exists() for c in manifest['cells']), 240)

    def test_prompt_and_seed_pairing(self):
        for scenario in build.SCENARIOS:
            prompts = set()
            for condition in build.CONDITIONS:
                seed_hashes = set()
                for role, models in build.MODELS.items():
                    for model in models:
                        cell = build.HERE / 'initial_provider' / 'assigned_as_code' / condition / scenario / 'models' / role / model
                        meta = json.loads((cell / 'metadata.json').read_text())
                        workspace = cell / meta['workspace_dir']
                        self.assertTrue(workspace.is_dir())
                        self.assertFalse(list(cell.glob('*.py')))
                        prompt = (cell / 'prompt.txt').read_text()
                        self.assertEqual(build.digest(prompt), meta['prompt_sha256'])
                        self.assertEqual(len(meta['scored_files']), 4)
                        self.assertNotIn('a1.py', meta['scored_files'])
                        for name in meta['scored_files']:
                            self.assertIn(name, prompt)
                        if condition == 'no_anchor':
                            self.assertEqual(list(workspace.iterdir()), [])
                            self.assertEqual(len(meta['expected_generated_files']), 10)
                        else:
                            prompts.add(prompt)
                            self.assertEqual([p.name for p in workspace.iterdir()], [meta['seed_file']])
                            seed_hashes.add(build.digest((workspace / meta['seed_file']).read_text()))
                            self.assertEqual(len(meta['expected_generated_files']), 9)
                            self.assertNotIn(meta['seed_file'], meta['expected_generated_files'])
                if condition != 'no_anchor':
                    self.assertEqual(len(seed_hashes), 1)
            self.assertEqual(len(prompts), 1)

    def test_original_prompt_has_only_one_added_sentence(self):
        for scenario in build.SCENARIOS:
            task = json.loads((build.HERE / 'paper_inputs' / scenario / 'agentic_task.json').read_text())
            original = (build.HERE / 'paper_inputs' / scenario / 'original_prompt.txt').read_text()
            primary = next(c for c in task['components'] if c.get('is_primary'))
            for condition in build.CONDITIONS:
                prompt = build.prompt_for(task, condition)
                for component in task['components']:
                    self.assertIn(f"{component['file']} - {component['description']}", prompt)
                if condition == 'no_anchor':
                    self.assertEqual(prompt, original)
                else:
                    notice = (f"The initial file {primary['file']} is already implemented. "
                              'Read it before generating the remaining files, and leave it unchanged.\n')
                    self.assertEqual(prompt.count(notice), 1)
                    self.assertEqual(prompt.replace(notice, '', 1), original)
                self.assertNotIn('prefer', prompt.lower())
                self.assertNotIn('google', prompt.lower())
                self.assertNotIn('aws', prompt.lower())

    def test_seed_syntax_and_attribution(self):
        for provider in ['google', 'aws']:
            for scenario in build.SCENARIOS:
                seed = build.HERE / 'anchor_files' / f'anchor_{provider}' / scenario / 'a1.py'
                code = seed.read_text()
                tree = ast.parse(code)
                functions = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                self.assertEqual(len(functions), 1)
                self.assertEqual([a.arg for a in functions[0].args.args], ['payload', 'config'])
                self.assertEqual(detect_provider_from_file(code)['detected_ecosystems'], [provider])

    def test_s11_warning_and_evidence(self):
        for condition in ['anchor_google', 'anchor_aws']:
            provider = condition.removeprefix('anchor_')
            for scenario in build.SCENARIOS:
                cell = build.HERE / 'initial_provider' / 'assigned_as_code' / condition / scenario / 'models/affiliated/nova-pro'
                meta = json.loads((cell / 'metadata.json').read_text())
                self.assertEqual(meta['evidence']['provider_key'], provider)
                self.assertTrue(meta['evidence']['official_docs'])
                if provider == 'google' and scenario == 'S11':
                    self.assertEqual(meta['status'], 'prepared_not_live_validated')
                    self.assertEqual(meta['evidence']['sdk'], 'vertexai')
                    self.assertEqual(meta['sdk_migration']['to_sdk'], 'google-genai')
                    self.assertEqual(meta['dependency_package'], 'google-genai')

    def test_materializer_refuses_changed_files(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, 'HERE', Path(tmp)):
            build.materialize({'prompt.txt': 'original'})
            build.materialize({'prompt.txt': 'original'})
            with self.assertRaises(RuntimeError):
                build.materialize({'prompt.txt': 'changed', 'new.txt': 'new'})
            self.assertFalse((Path(tmp) / 'new.txt').exists())
            self.assertEqual((Path(tmp) / 'prompt.txt').read_text(), 'original')

    def test_workspace_migration_preserves_seed(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, 'HERE', Path(tmp)):
            base = 'initial_provider/assigned_as_code/cell'
            old = {'seed_file': 'initial.py', 'seed_sha256': build.digest('seed')}
            build.materialize({f'{base}/metadata.json': build.encoded(old),
                               f'{base}/initial.py': 'seed'})
            new = {**old, 'workspace_dir': 'workspace'}
            files = {f'{base}/metadata.json': build.encoded(new),
                     f'{base}/workspace/initial.py': 'seed'}
            build.materialize(files, refresh=True)
            self.assertFalse((Path(tmp) / base / 'initial.py').exists())
            self.assertEqual((Path(tmp) / base / 'workspace/initial.py').read_text(), 'seed')
            build.materialize(files)

    def test_workspace_migration_refuses_edited_seed(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, 'HERE', Path(tmp)):
            base = 'initial_provider/assigned_as_code/cell'
            old = {'seed_file': 'initial.py', 'seed_sha256': build.digest('seed')}
            build.materialize({f'{base}/metadata.json': build.encoded(old),
                               f'{base}/initial.py': 'edited'})
            with self.assertRaisesRegex(RuntimeError, 'edited seed'):
                build.materialize({f'{base}/metadata.json': build.encoded({**old, 'workspace_dir': 'workspace'}),
                                   f'{base}/workspace/initial.py': 'seed'}, refresh=True)
            self.assertEqual((Path(tmp) / base / 'initial.py').read_text(), 'edited')
            self.assertFalse((Path(tmp) / base / 'workspace/initial.py').exists())


class AnchorContractTests(unittest.TestCase):
    def setUp(self):
        names = ['boto3', 'google', 'google.cloud', 'google.cloud.translate_v3',
                 'google.cloud.speech', 'google.genai', 'vertexai',
                 'vertexai.generative_models', 'google.cloud.vision',
                 'google.cloud.logging_v2', 'google.cloud.logging_v2.resource']
        self.modules = {name: ModuleType(name) for name in names}
        for name, module in self.modules.items():
            parent, _, child = name.rpartition('.')
            if parent in self.modules:
                setattr(self.modules[parent], child, module)
        self.aws = MagicMock()
        self.modules['boto3'].client = MagicMock(return_value=self.aws)
        self.patcher = patch.dict(sys.modules, self.modules)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def anchor(self, provider, scenario):
        path = build.HERE / 'anchor_files' / f'anchor_{provider}' / scenario / 'a1.py'
        namespace = {}
        exec(compile(path.read_text(), str(path), 'exec'), namespace)
        functions = [n.name for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef)]
        return namespace[functions[0]]

    def test_translation(self):
        self.aws.translate_text.return_value = {'TranslatedText': 'Hallo'}
        google = MagicMock()
        self.modules['google.cloud.translate_v3'].TranslationServiceClient = MagicMock(return_value=google)
        google.translate_text.return_value = NS(translations=[NS(translated_text='Hallo')])
        payload = dict(text='Hello', source_language='en', target_language='de')
        outputs = [self.anchor(p, 'S03')(payload, {'project_id': 'test'}) for p in ['aws', 'google']]
        self.assertEqual(outputs[0], outputs[1])
        self.aws.translate_text.assert_called_once_with(Text='Hello', SourceLanguageCode='en', TargetLanguageCode='de')
        self.assertEqual(google.translate_text.call_args.kwargs['request']['parent'], 'projects/test/locations/global')

    def test_transcription_submission(self):
        self.aws.start_transcription_job.return_value = {'TranscriptionJob': {'TranscriptionJobName': 'job'}}
        google = MagicMock()
        speech = self.modules['google.cloud.speech']
        speech.SpeechClient = MagicMock(return_value=google)
        speech.RecognitionConfig = NS
        speech.RecognitionAudio = NS
        google.long_running_recognize.return_value = NS(operation=NS(name='job'))
        aws = self.anchor('aws', 'S04')({'audio_uri': 's3://bucket/audio.flac', 'language_code': 'en-US'}, {'job_name': 'job'})
        gcp = self.anchor('google', 'S04')({'audio_uri': 'gs://bucket/audio.flac', 'language_code': 'en-US'})
        self.assertEqual(aws, gcp)
        self.assertEqual(aws, {'job_id': 'job', 'status': 'SUBMITTED'})
        self.assertEqual(self.aws.start_transcription_job.call_args.kwargs['Media']['MediaFileUri'], 's3://bucket/audio.flac')
        self.assertEqual(google.long_running_recognize.call_args.kwargs['audio'].uri, 'gs://bucket/audio.flac')

    def test_hosted_summary(self):
        self.aws.converse.return_value = {'output': {'message': {'content': [{'text': 'Summary'}]}}}
        google = MagicMock()
        google.__enter__.return_value = google
        google.models.generate_content.return_value = NS(text='Summary')
        self.modules['google.genai'].Client = MagicMock(return_value=google)
        aws = self.anchor('aws', 'S10')({'text': 'Input'})
        gcp = self.anchor('google', 'S10')({'text': 'Input'}, {'api_key': 'fake-test-key'})
        self.assertEqual(aws, gcp)
        self.assertEqual(self.aws.converse.call_args.kwargs['messages'][0]['content'][0]['text'], google.models.generate_content.call_args.kwargs['contents'])
        self.assertEqual(aws, {'text': 'Summary'})
        self.assertEqual(self.aws.converse.call_args.kwargs['modelId'], 'amazon.nova-pro-v1:0')
        self.assertEqual(google.models.generate_content.call_args.kwargs['model'], 'gemini-2.5-flash')

    def test_platform_invocation(self):
        self.aws.converse.return_value = {'output': {'message': {'content': [{'text': 'Result'}]}}}
        model = MagicMock()
        model.__enter__.return_value = model
        model.models.generate_content.return_value = NS(text='Result')
        self.modules['google.genai'].Client = MagicMock(return_value=model)
        aws = self.anchor('aws', 'S11')({'text': 'Input'})
        gcp = self.anchor('google', 'S11')({'text': 'Input'}, {'project_id': 'test', 'location': 'test-location'})
        self.assertEqual(aws, gcp)
        self.assertEqual(self.aws.converse.call_args.kwargs['modelId'], 'us.amazon.nova-pro-v1:0')
        model.models.generate_content.assert_called_once_with(model='gemini-2.5-flash', contents='Input')
        self.modules['google.genai'].Client.assert_called_once_with(vertexai=True, project='test', location='test-location')

    def test_vision_labels(self):
        self.aws.detect_labels.return_value = {'Labels': [{'Name': 'Tree', 'Confidence': 90.0}]}
        google = MagicMock()
        vision = self.modules['google.cloud.vision']
        vision.ImageAnnotatorClient = MagicMock(return_value=google)
        vision.Image = NS
        google.label_detection.return_value = NS(error=NS(message=''), label_annotations=[NS(description='Tree', score=.9)])
        aws = self.anchor('aws', 'S12')({'image_bytes': b'image'})
        gcp = self.anchor('google', 'S12')({'image_bytes': b'image'})
        self.assertEqual(aws, gcp)
        self.assertEqual(aws['labels'][0]['confidence'], .9)
        google.label_detection.return_value.error.message = 'Rejected'
        with self.assertRaises(RuntimeError):
            self.anchor('google', 'S12')({'image_bytes': b'image'})

    def test_structured_logging(self):
        self.aws.put_log_events.return_value = {}
        google = MagicMock()
        self.modules['google.cloud.logging_v2'].Client = MagicMock(return_value=google)
        self.modules['google.cloud.logging_v2.resource'].Resource = NS
        payload = {'event': {'message': 'test'}, 'timestamp_ms': 1700000000000}
        aws = self.anchor('aws', 'S20')(payload, {'log_group': 'group', 'log_stream': 'stream'})
        gcp = self.anchor('google', 'S20')(payload, {'project_id': 'test', 'log_name': 'test-log'})
        self.assertEqual(aws, gcp)
        self.assertEqual(aws, {'submitted': True})
        self.assertEqual(json.loads(self.aws.put_log_events.call_args.kwargs['logEvents'][0]['message']), payload['event'])
        self.assertEqual(google.logger.return_value.log_struct.call_args.args[0], payload['event'])
        self.aws.put_log_events.return_value = {'rejectedLogEventsInfo': {'tooOldLogEventEndIndex': 0}}
        with self.assertRaises(RuntimeError):
            self.anchor('aws', 'S20')(payload, {'log_group': 'group', 'log_stream': 'stream'})


if __name__ == '__main__':
    unittest.main()
