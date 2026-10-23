from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk

def normalize_request(payload):
    return {
        'language_code': payload.get('language_code', 'en-US'),
        'sample_rate_hz': payload.get('sample_rate_hz', 16000),
        'audio_chunks': payload.get('audio_chunks', [])
    }

def normalize_response(event):
    return {
        'text': event['text'],
        'is_final': event['is_final']
    }