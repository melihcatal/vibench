"""Offline extension checks; never invoke models or cloud services."""
import ast
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import secrets
import sys
import time
from types import SimpleNamespace as NS
import unittest
from unittest.mock import MagicMock, patch
import uuid

CODE = Path(__file__).resolve().parents[5]   # import root
ROOT = CODE.parent                           # repo root, as code_sha256 keys are written
sys.path.insert(0, str(CODE))
from ablations.initial_provider.assigned_as_code.microsoft_openai.scripts import build_inputs, run as a1
from ablations.initial_provider.by_instruction.microsoft_openai.scripts import run as a3
from ablations.shared import campaign, scoring
from ablations.shared.common import sha


def function(scenario, namespace):
    tree = ast.parse((build_inputs.BASE / 'templates' / scenario / 'a1.py').read_text())
    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    scope = dict(json=json, os=os, secrets=secrets, io=io, datetime=datetime,
                 timezone=timezone, timedelta=timedelta, time=time, uuid=uuid)
    scope.update(namespace)
    exec(compile(tree, scenario, 'exec'), scope)
    return next(scope[node.name] for node in tree.body if isinstance(node, ast.FunctionDef))


class ExtensionTests(unittest.TestCase):
    def test_inputs_and_prompt_differences(self):
        for path, value in build_inputs.desired_files().items():
            self.assertEqual(path.read_text(), value)
        for sid in build_inputs.SCENARIOS:
            old = (CODE / f'ablations/paper_inputs/{sid}/original_prompt.txt').read_text()
            for runner, condition in ((a1, 'anchor_microsoft_openai'), (a3, 'instruct_microsoft_openai')):
                data = runner.cell_inputs(condition, sid, 'gpt-5.4-mini')
                lines = data['prompt'].splitlines(keepends=True)
                self.assertEqual(''.join(lines[:1] + lines[2:]), old)
                scores = scoring.score_files(data['task'], {})
                self.assertEqual(scores['groups']['explicit']['downstream']['expected'], 4)
                self.assertEqual(scores['groups']['explicit']['aligned_core']['expected'], 3 if runner is a1 else 4)
                self.assertEqual(data['seed'] is None, runner is a3)
            old_seed = CODE / f'ablations/anchor_files/anchor_google/{sid}/a1.py'
            old_fn = next(n for n in ast.parse(old_seed.read_text()).body if isinstance(n, ast.FunctionDef))
            new_fn = next(n for n in ast.parse((build_inputs.BASE / 'templates' / sid / 'a1.py').read_text()).body if isinstance(n, ast.FunctionDef))
            self.assertEqual(old_fn.name, new_fn.name)
            self.assertEqual(ast.dump(old_fn.args), ast.dump(new_fn.args))

    def test_plans_and_reasoning(self):
        for runner in (a1, a3):
            args = runner.parser().parse_args([])
            plan = campaign.make_plan(args, runner.CONDITIONS, runner.cell_inputs)
            self.assertEqual(len(plan['cells']), 300)
            self.assertEqual(plan['timeout'], 300)
            self.assertEqual({c['condition'] for c in plan['cells']}, set(runner.CONDITIONS))
            self.assertEqual({c['repetition'] for c in plan['cells']}, {1, 2, 3, 4, 5})
            self.assertEqual(plan['sampling'], a1.configuration.paper_sampling())
            self.assertIn(str(Path(runner.__file__).relative_to(ROOT)), plan['code_sha256'])

    def test_request_contracts(self):
        requests = MagicMock()
        msal = MagicMock()
        msal.ConfidentialClientApplication.return_value.acquire_token_for_client.return_value = {'access_token': 'test-token'}
        requests.post.return_value.json.return_value = {'id': 'user'}
        result = function('S01', {'requests': requests, 'msal': msal})(
            {'email': 'test@example.org', 'password': 'test-only'},
            {'client_id': 'id', 'tenant_id': 'tenant', 'client_secret': 'test-only', 'issuer': 'tenant.onmicrosoft.com'})
        self.assertEqual(result, {'user_id': 'user'})
        self.assertEqual(requests.post.call_args.kwargs['json']['identities'][0]['signInType'], 'emailAddress')
        msal.ConfidentialClientApplication.return_value.get_authorization_request_url.return_value = 'auth-url'
        result = function('S02', {'msal': msal})({'redirect_uri': 'https://example.org/callback'},
            {'client_id': 'id', 'tenant_id': 'tenant', 'client_secret': 'test-only'})
        self.assertEqual(result['authorization_url'], 'auth-url')
        self.assertTrue(result['session_id'])
        requests.post.return_value.json.return_value = [{'translations': [{'text': 'Hallo'}]}]
        self.assertEqual(function('S03', {'requests': requests})(
            {'text': 'Hello', 'source_language': 'en', 'target_language': 'de'},
            {'api_key': 'test-only', 'region': 'region'})['text'], 'Hallo')
        requests.post.return_value.json.return_value = {'self': 'job-url'}
        self.assertEqual(function('S04', {'requests': requests})(
            {'audio_uri': 'https://example.org/audio.wav', 'language_code': 'en-US'},
            {'api_key': 'test-only', 'region': 'region'}), {'job_id': 'job-url', 'status': 'SUBMITTED'})
        self.assertEqual(requests.post.call_args.kwargs['json']['contentUrls'], ['https://example.org/audio.wav'])

    def test_openai_contracts(self):
        factory = MagicMock()
        client = factory.return_value.__enter__.return_value
        client.embeddings.create.return_value = NS(data=[NS(embedding=[0.1, 0.2])])
        client.chat.completions.create.return_value = NS(choices=[NS(message=NS(content='result'))])
        self.assertEqual(function('S09', {'OpenAI': factory})({'text': 'text'}, {'api_key': 'test-only'}), {'embedding': [0.1, 0.2]})
        self.assertEqual(function('S10', {'OpenAI': factory})({'text': 'text'}, {'api_key': 'test-only'}), {'text': 'result'})
        self.assertEqual(client.chat.completions.create.call_args.kwargs['model'], 'gpt-5.4-mini')
        self.assertEqual(function('S11', {'AzureOpenAI': factory})({'text': 'text'},
            {'endpoint': 'https://test.openai.azure.com', 'api_key': 'test-only', 'deployment': 'test-deployment'}), {'text': 'result'})
        self.assertEqual(factory.call_args.kwargs['api_version'], '2024-10-21')

    def test_document_and_vision_contracts(self):
        factory, credential = MagicMock(), MagicMock()
        client = factory.return_value.__enter__.return_value
        client.begin_analyze_document.return_value.result.return_value = NS(content='scan')
        namespace = {'DocumentIntelligenceClient': factory, 'AzureKeyCredential': credential}
        payload = {'document_bytes': b'scan', 'mime_type': 'image/png'}
        config = {'endpoint': 'endpoint', 'api_key': 'test-only'}
        self.assertEqual(function('S07', namespace)(payload, config), {'text': 'scan'})
        client.begin_analyze_document.return_value.result.return_value = NS(documents=[NS(fields={
            'VendorName': NS(content='vendor'), 'Items': NS(value_array=[NS(value_object={'Description': NS(content='item')})])})])
        invoice = function('S08', namespace)(payload, config)['invoices'][0]
        self.assertEqual(invoice['vendor'], 'vendor')
        self.assertEqual(invoice['line_items'][0], {'description': 'item', 'quantity': None, 'amount': None})
        client.analyze.return_value = NS(tags=NS(list=[NS(name='label', confidence=0.8)]))
        result = function('S12', {'ImageAnalysisClient': factory, 'AzureKeyCredential': credential,
                                  'VisualFeatures': NS(TAGS='tags')})({'image_bytes': b'image'}, config)
        self.assertEqual(result, {'labels': [{'name': 'label', 'confidence': 0.8}]})
        client.analyze_text.return_value = NS(categories_analysis=[NS(severity=4), NS(severity=2)])
        result = function('S13', {'ContentSafetyClient': factory, 'AzureKeyCredential': credential,
                                  'AnalyzeTextOptions': MagicMock()})({'text': 'text'}, config)
        self.assertAlmostEqual(result['toxicity'], 4 / 7)

    def test_storage_security_and_observability_contracts(self):
        factory, credential = MagicMock(), MagicMock()
        client = factory.return_value.__enter__.return_value
        ns = {'DefaultAzureCredential': credential}
        self.assertEqual(function('S14', dict(ns, BlobServiceClient=factory, ContentSettings=MagicMock()))(
            {'data': b'body', 'object_name': 'object'}, {'account_url': 'url', 'container': 'container'}), {'object_name': 'object'})
        self.assertEqual(function('S15', {'CosmosClient': factory})(
            {'id': 'id', 'document': {'value': 1}}, {'endpoint': 'url', 'api_key': 'test-only', 'database': 'db', 'container': 'container'}), {'id': 'id'})
        client.get_secret.return_value = NS(value='{"key":"test-value"}')
        self.assertEqual(function('S16', dict(ns, SecretClient=factory))(
            {'secret_id': 'secret', 'key_field': 'key'}, {'vault_url': 'url'}), {'api_key': 'test-value'})
        client.encrypt.return_value = NS(ciphertext=b'cipher', iv=b'iv', authentication_tag=b'tag', key_id='key')
        result = function('S17', dict(ns, CryptographyClient=factory, EncryptionAlgorithm=NS(a256_gcm='A256GCM')))(
            {'plaintext': b'plain'}, {'key_id': 'key'})
        self.assertEqual(result['tag'], b'tag')
        service = MagicMock()
        message = MagicMock()
        result = function('S18', {'ServiceBusClient': service, 'ServiceBusMessage': message})(
            {'event': {'value': 1}}, {'connection_string': 'test-only', 'topic': 'topic'})
        self.assertEqual(message.call_args.kwargs['message_id'], result['message_id'])
        client.query_resource.return_value = NS(metrics=[NS(timeseries=[NS(data=[
            NS(timestamp=datetime.fromtimestamp(1, tz=timezone.utc), average=2), NS(average=None)])])])
        result = function('S19', dict(ns, MetricsQueryClient=factory, MetricAggregationType=NS(AVERAGE='Average')))(
            {'metric': 'metric', 'start_time': 0, 'end_time': 60}, {'resource_id': 'resource'})
        self.assertEqual(result, {'points': [{'timestamp': 1.0, 'value': 2.0}]})
        result = function('S20', dict(ns, LogsIngestionClient=factory))(
            {'event': {'value': 1}, 'timestamp_ms': 1000}, {'endpoint': 'url', 'rule_id': 'rule', 'stream_name': 'stream'})
        self.assertEqual(result, {'submitted': True})
        self.assertEqual(client.upload.call_args.kwargs['logs'][0]['TimeGenerated'], '1970-01-01T00:00:01+00:00')

    def test_speech_contracts(self):
        from queue import Queue
        from threading import Thread
        speech = MagicMock()
        recognizer = speech.SpeechRecognizer.return_value
        stream = speech.audio.PushAudioInputStream.return_value
        callbacks = {}
        for name in ('recognizing', 'recognized', 'session_stopped', 'canceled'):
            getattr(recognizer, name).connect.side_effect = lambda fn, name=name: callbacks.update({name: fn})
        stream.close.side_effect = lambda: callbacks['session_stopped'](None)
        stream.write.side_effect = lambda chunk: callbacks['recognized'](NS(result=NS(
            text='transcript', reason=speech.ResultReason.RecognizedSpeech)))
        stream_fn = function('S05', {'speechsdk': speech, 'Queue': Queue, 'Thread': Thread})
        self.assertEqual(list(stream_fn({'audio_chunks': [b'pcm'], 'sample_rate_hz': 16000,
            'language_code': 'en-US'}, {'api_key': 'test-only', 'region': 'region'})),
            [{'text': 'transcript', 'is_final': True}])
        speech.SpeechSynthesizer.return_value.speak_text_async.return_value.get.return_value = NS(
            reason=speech.ResultReason.SynthesizingAudioCompleted, audio_data=b'mp3')
        self.assertEqual(function('S06', {'speechsdk': speech})({'text': 'text'},
            {'api_key': 'test-only', 'region': 'region'}), {'audio_bytes': b'mp3', 'content_type': 'audio/mpeg'})


if __name__ == '__main__':
    unittest.main()
