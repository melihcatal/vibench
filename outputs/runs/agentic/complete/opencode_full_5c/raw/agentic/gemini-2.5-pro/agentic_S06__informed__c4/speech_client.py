import os
from google.cloud import texttospeech


def get_speech_client():
    """Initializes and returns a Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()
