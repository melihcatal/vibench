import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    return speech.SpeechClient()


def get_streaming_config(language_code="en-US", enable_automatic_punctuation=True):
    return speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        ),
        interim_results=True,
    )
