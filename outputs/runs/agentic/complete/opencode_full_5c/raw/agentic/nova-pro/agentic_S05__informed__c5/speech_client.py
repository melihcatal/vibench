import os
from google.cloud import speech_v1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = speech.SpeechClient()


def get_speech_client():
    return client


def create_streaming_config(language_code="en-US", sample_rate_hertz=16000):
    return speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
        ),
        interim_results=True,
    )
