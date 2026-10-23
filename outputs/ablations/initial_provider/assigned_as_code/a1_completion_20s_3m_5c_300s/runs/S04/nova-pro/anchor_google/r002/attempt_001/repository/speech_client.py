import os

from google.cloud import speech


def get_speech_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return speech.SpeechClient()


def get_transcription_config(language_code):
    return speech.RecognitionConfig(language_code=language_code)