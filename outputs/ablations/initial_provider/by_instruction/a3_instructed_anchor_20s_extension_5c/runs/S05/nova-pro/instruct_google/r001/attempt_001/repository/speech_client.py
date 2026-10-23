import os
from google.cloud import speech

def get_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    return speech.SpeechClient()

def streaming_config(language_code='en-US', sample_rate_hertz=16000):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    return config