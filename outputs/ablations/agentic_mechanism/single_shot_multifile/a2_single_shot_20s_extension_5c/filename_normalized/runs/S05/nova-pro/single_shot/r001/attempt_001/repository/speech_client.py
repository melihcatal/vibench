import os
from google.cloud import speech

def get_streaming_client():
    client = speech.SpeechClient()
    return client

def create_config(language_code, enable_automatic_punctuation):
    config = {
        'encoding': 'LINEAR16',
       'sample_rate_hertz': 16000,
        'language_code': language_code,
        'enable_automatic_punctuation': enable_automatic_punctuation,
    }
    return config

def start_stream(config):
    request = {
        'config': config,
        'interim_results': True,
    }
    stream = client.streaming_recognize(request)
    return stream

def stream_audio(data):
    request = {
        'content': data,
    }
    response = next(stream)
    return response
