"""Offline service-contract tests for the 14 additional paired anchors."""
import ast
import asyncio
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace as NS
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ablations.shared.common import HERE


class ExpandedAnchors(unittest.TestCase):
    def setUp(self):
        names = ['boto3', 'requests', 'firebase_admin', 'firebase_admin.auth', 'google',
                 'google.genai', 'google.cloud', 'google.cloud.speech', 'google.cloud.texttospeech',
                 'google.cloud.documentai', 'google.cloud.storage', 'google.cloud.firestore',
                 'google.cloud.secretmanager', 'google.cloud.kms', 'google.cloud.pubsub_v1',
                 'google.cloud.monitoring_v3', 'amazon_transcribe', 'amazon_transcribe.client']
        self.modules = {name: ModuleType(name) for name in names}
        for name, module in self.modules.items():
            parent, _, child = name.rpartition('.')
            if parent in self.modules:
                setattr(self.modules[parent], child, module)
        self.aws = MagicMock()
        self.modules['boto3'].client = MagicMock(return_value=self.aws)
        self.modules['boto3'].resource = MagicMock(return_value=self.aws)
        self.modules['boto3'].Session = MagicMock(return_value=NS(region_name='us-east-1'))
        self.http = MagicMock()
        self.modules['requests'].post = MagicMock(return_value=self.http)
        patcher = patch.dict(sys.modules, self.modules)
        patcher.start()
        self.addCleanup(patcher.stop)

    def anchor(self, provider, sid):
        path = HERE / 'anchor_files' / f'anchor_{provider}' / sid / 'a1.py'
        code = path.read_text()
        namespace = {}
        exec(compile(code, str(path), 'exec'), namespace)
        function = next(n.name for n in ast.parse(code).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
        return namespace[function]

    def client(self, module, name):
        client = MagicMock()
        client.__enter__.return_value = client
        setattr(self.modules[module], name, MagicMock(return_value=client))
        return client

    def test_registration(self):
        self.aws.sign_up.return_value = {'UserSub': 'u1'}
        firebase = self.modules['firebase_admin']
        firebase.get_app = MagicMock(side_effect=ValueError())
        firebase.initialize_app = MagicMock(return_value='app')
        self.modules['firebase_admin.auth'].create_user = MagicMock(return_value=NS(uid='u1'))
        payload = {'email': 'test@example.com', 'password': 'test-only-password'}
        aws = self.anchor('aws', 'S01')(payload, {'client_id': 'client', 'client_secret': 'secret'})
        google = self.anchor('google', 'S01')(payload, {'project_id': 'test'})
        self.assertEqual(aws, google)
        self.assertIn('SecretHash', self.aws.sign_up.call_args.kwargs)
        firebase.initialize_app.assert_called_once_with(options={'projectId': 'test'})

    def test_federation(self):
        payload = {'redirect_uri': 'https://example.com/callback'}
        aws = self.anchor('aws', 'S02')(payload, {'domain_prefix': 'test', 'region': 'us-east-1', 'client_id': 'client'})
        url = urlparse(aws['authorization_url'])
        self.assertEqual(url.netloc, 'test.auth.us-east-1.amazoncognito.com')
        self.assertEqual(parse_qs(url.query)['response_type'], ['code'])
        self.assertEqual(parse_qs(url.query)['state'], [aws['session_id']])
        self.http.json.return_value = {'authUri': 'https://idp.example/auth', 'sessionId': 'binding'}
        result = self.anchor('google', 'S02')(payload, {'provider_id': 'oidc.test', 'api_key': 'test'})
        self.assertEqual(result, {'authorization_url': 'https://idp.example/auth', 'session_id': 'binding'})
        call = self.modules['requests'].post.call_args
        self.assertEqual(call.args[0], 'https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri')
        self.assertEqual(call.kwargs['json']['providerId'], 'oidc.test')
        self.http.raise_for_status.assert_called_once()

    def test_streaming(self):
        expected = [{'text': 'partial', 'is_final': False}, {'text': 'final', 'is_final': True}]
        async def output():
            for row in expected:
                await asyncio.sleep(0)
                yield NS(transcript=NS(results=[NS(alternatives=[NS(transcript=row['text'])], is_partial=not row['is_final'])]))
        stream = NS(input_stream=NS(send_audio_event=AsyncMock(), end_stream=AsyncMock()), output_stream=output())
        aws = self.client('amazon_transcribe.client', 'TranscribeStreamingClient')
        aws.start_stream_transcription = AsyncMock(return_value=stream)
        payload = {'audio_chunks': [b'pcm1', b'pcm2'], 'sample_rate_hz': 16000, 'language_code': 'en-US'}
        async def collect():
            return [row async for row in self.anchor('aws', 'S05')(payload)]
        self.assertEqual(asyncio.run(collect()), expected)
        self.assertEqual(stream.input_stream.send_audio_event.await_count, 2)
        stream.input_stream.end_stream.assert_awaited_once()
        speech = self.modules['google.cloud.speech']
        speech.RecognitionConfig = MagicMock(side_effect=lambda **kwargs: NS(**kwargs))
        speech.RecognitionConfig.AudioEncoding = NS(LINEAR16=1)
        speech.StreamingRecognitionConfig = NS
        speech.StreamingRecognizeRequest = NS
        google = self.client('google.cloud.speech', 'SpeechClient')
        google.streaming_recognize.return_value = [NS(results=[NS(alternatives=[NS(transcript=r['text'])], is_final=r['is_final'])]) for r in expected]
        self.assertEqual(list(self.anchor('google', 'S05')(payload)), expected)
        requests = list(google.streaming_recognize.call_args.kwargs['requests'])
        self.assertEqual([r.audio_content for r in requests], payload['audio_chunks'])

    def test_synthesis(self):
        stream = io.BytesIO(b'audio')
        self.aws.synthesize_speech.return_value = {'AudioStream': stream}
        speech = self.modules['google.cloud.texttospeech']
        speech.SynthesisInput = speech.VoiceSelectionParams = speech.AudioConfig = NS
        speech.AudioEncoding = NS(MP3=1)
        google = self.client('google.cloud.texttospeech', 'TextToSpeechClient')
        google.synthesize_speech.return_value = NS(audio_content=b'audio')
        self.assertEqual(self.anchor('aws', 'S06')({'text': 'Hello'}), self.anchor('google', 'S06')({'text': 'Hello'}))
        self.assertTrue(stream.closed)

    def document_client(self, document):
        self.modules['google.cloud.documentai'].RawDocument = NS
        client = self.client('google.cloud.documentai', 'DocumentProcessorServiceClient')
        client.process_document.return_value = NS(document=document)
        client.processor_path.return_value = 'processor'
        return client

    def test_ocr(self):
        self.aws.detect_document_text.return_value = {'Blocks': [{'BlockType': 'LINE', 'Text': 'Hello'}, {'BlockType': 'WORD', 'Text': 'Hello'}]}
        google = self.document_client(NS(text='Hello'))
        payload = {'document_bytes': b'image', 'mime_type': 'image/png'}
        self.assertEqual(self.anchor('aws', 'S07')(payload), self.anchor('google', 'S07')(payload,
            {'project_id': 'test', 'location': 'us', 'processor_id': 'ocr'}))
        self.assertEqual(google.process_document.call_args.kwargs['request']['raw_document'].content, b'image')

    def test_invoice(self):
        def field(name, value):
            return {'Type': {'Text': name}, 'ValueDetection': {'Text': value}}
        self.aws.analyze_expense.return_value = {'ExpenseDocuments': [{
            'SummaryFields': [field('VENDOR_NAME', 'Shop'), field('INVOICE_RECEIPT_DATE', '2026-01-01'), field('TOTAL', '12')],
            'LineItemGroups': [{'LineItems': [{'LineItemExpenseFields': [field('ITEM', 'Widget'), field('QUANTITY', '2'), field('PRICE', '12')]}]}]}]}
        self.document_client(NS(entities=[NS(type_='supplier_name', mention_text='Shop'), NS(type_='invoice_date', mention_text='2026-01-01'),
            NS(type_='total_amount', mention_text='12'), NS(type_='line_item', properties=[NS(type_='line_item/description', mention_text='Widget'),
                NS(type_='line_item/quantity', mention_text='2'), NS(type_='line_item/amount', mention_text='12')])]))
        payload = {'document_bytes': b'image', 'mime_type': 'image/png'}
        self.assertEqual(self.anchor('aws', 'S08')(payload), self.anchor('google', 'S08')(payload,
            {'project_id': 'test', 'location': 'us', 'processor_id': 'invoice'}))

    def test_embeddings(self):
        stream = io.BytesIO(b'{"embedding":[0.1,0.2]}')
        self.aws.invoke_model.return_value = {'body': stream}
        google = self.client('google.genai', 'Client')
        google.models.embed_content.return_value = NS(embeddings=[NS(values=[.1, .2])])
        self.assertEqual(self.anchor('aws', 'S09')({'text': 'Hello'}), self.anchor('google', 'S09')({'text': 'Hello'}, {'api_key': 'fake'}))
        self.assertTrue(stream.closed)
        self.assertEqual(self.aws.invoke_model.call_args.kwargs['modelId'], 'amazon.titan-embed-text-v2:0')

    def test_moderation(self):
        self.aws.detect_toxic_content.return_value = {'ResultList': [{'Toxicity': .2}]}
        self.http.json.return_value = {'attributeScores': {'TOXICITY': {'summaryScore': {'value': .2}}}}
        self.assertEqual(self.anchor('aws', 'S13')({'text': 'hello'}), self.anchor('google', 'S13')({'text': 'hello'}, {'api_key': 'fake'}))
        self.assertTrue(self.modules['requests'].post.call_args.kwargs['json']['doNotStore'])
        self.http.raise_for_status.assert_called_once()

    def test_storage(self):
        google = self.client('google.cloud.storage', 'Client')
        payload = {'object_name': 'object', 'data': b'bytes'}
        self.assertEqual(self.anchor('aws', 'S14')(payload, {'bucket': 'test'}),
                         self.anchor('google', 'S14')(payload, {'bucket': 'test', 'project_id': 'test'}))
        self.assertEqual(google.bucket.return_value.blob.return_value.upload_from_file.call_args.args[0].getvalue(), b'bytes')

    def test_document_upsert(self):
        self.client('google.cloud.firestore', 'Client')
        payload = {'id': 'doc', 'document': {'value': 1.5}}
        self.assertEqual(self.anchor('aws', 'S15')(payload, {'table_name': 'test'}),
                         self.anchor('google', 'S15')(payload, {'project_id': 'test', 'collection': 'test'}))
        from decimal import Decimal
        self.assertEqual(self.aws.Table.return_value.put_item.call_args.kwargs['Item']['value'], Decimal('1.5'))

    def test_secrets(self):
        self.aws.get_secret_value.return_value = {'SecretString': '{"token":"test-only"}'}
        google = self.client('google.cloud.secretmanager', 'SecretManagerServiceClient')
        google.access_secret_version.return_value = NS(payload=NS(data=b'{"token":"test-only"}'))
        payload = {'secret_id': 'secret', 'key_field': 'token'}
        self.assertEqual(self.anchor('aws', 'S16')(payload), self.anchor('google', 'S16')(payload, {'project_id': 'test'}))
        self.assertEqual(google.access_secret_version.call_args.kwargs['request']['name'], 'projects/test/secrets/secret/versions/latest')

    def test_encryption(self):
        self.aws.encrypt.return_value = {'CiphertextBlob': b'cipher'}
        google = self.client('google.cloud.kms', 'KeyManagementServiceClient')
        google.encrypt.return_value = NS(ciphertext=b'cipher')
        payload = {'plaintext': b'plain'}
        self.assertEqual(self.anchor('aws', 'S17')(payload, {'key_id': 'key'}),
                         self.anchor('google', 'S17')(payload, {'key_id': 'key', 'project_id': 'test', 'location': 'global', 'key_ring': 'ring'}))

    def test_pubsub(self):
        self.aws.publish.return_value = {'MessageId': 'message'}
        google = self.client('google.cloud.pubsub_v1', 'PublisherClient')
        google.publish.return_value.result.return_value = 'message'
        payload = {'event': {'value': 1}}
        self.assertEqual(self.anchor('aws', 'S18')(payload, {'topic_arn': 'topic'}),
                         self.anchor('google', 'S18')(payload, {'project_id': 'test', 'topic_id': 'topic'}))
        google.stop.assert_called_once()
        self.assertEqual(json.loads(google.publish.call_args.args[1]), payload['event'])

    def test_metrics(self):
        time = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.aws.get_metric_statistics.return_value = {'Datapoints': [{'Timestamp': time, 'Average': 2.5}]}
        module = self.modules['google.cloud.monitoring_v3']
        module.Aggregation = NS(Aligner=NS(ALIGN_MEAN=1))
        module.ListTimeSeriesRequest = NS(TimeSeriesView=NS(FULL=1))
        google = self.client('google.cloud.monitoring_v3', 'MetricServiceClient')
        google.list_time_series.return_value = [NS(points=[NS(interval=NS(end_time=time),
            value=NS(_pb=NS(WhichOneof=lambda _: 'double_value'), double_value=2.5))])]
        payload = {'metric': 'example', 'start_time': time.timestamp() - 60, 'end_time': time.timestamp()}
        self.assertEqual(self.anchor('aws', 'S19')(payload, {'namespace': 'test'}),
                         self.anchor('google', 'S19')(payload, {'project_id': 'test'}))


if __name__ == '__main__':
    unittest.main()
