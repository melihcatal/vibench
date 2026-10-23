import os
from google.cloud import speech

speech_client = speech.SpeechClient()

def create_streaming_config(language_code='en-US'):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    return speech.StreamingRecognitionConfig(config=config)