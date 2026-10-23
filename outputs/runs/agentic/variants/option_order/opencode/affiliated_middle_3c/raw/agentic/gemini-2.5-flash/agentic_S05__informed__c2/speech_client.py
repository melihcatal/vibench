import os
from google.cloud import speech


def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or credentials should be passed explicitly.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.
    return speech.SpeechClient()
