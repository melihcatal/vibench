import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return speech.SpeechClient()


def create_streaming_config(language_code="en-US"):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )
    return speech.StreamingRecognitionConfig(config=config)
