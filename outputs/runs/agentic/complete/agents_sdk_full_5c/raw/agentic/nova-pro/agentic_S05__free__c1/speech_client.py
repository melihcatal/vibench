import os
from google.cloud import speech

def get_client():
    return speech.SpeechClient()

def get_config():
    return {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': 'en-US',
    }

def get_streaming_config(config):
    return types.StreamingRecognitionConfig(config=config, interim_results=True)