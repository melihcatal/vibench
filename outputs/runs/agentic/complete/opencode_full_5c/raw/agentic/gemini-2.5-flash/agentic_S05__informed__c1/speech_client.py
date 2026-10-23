import os
from google.cloud import speech


def get_speech_client():
    """
    Returns a Google Cloud Speech-to-Text client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    """
    return speech.SpeechClient()
