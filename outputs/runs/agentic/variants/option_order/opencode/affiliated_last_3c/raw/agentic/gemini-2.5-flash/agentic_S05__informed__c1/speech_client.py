import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return speech.SpeechClient()
