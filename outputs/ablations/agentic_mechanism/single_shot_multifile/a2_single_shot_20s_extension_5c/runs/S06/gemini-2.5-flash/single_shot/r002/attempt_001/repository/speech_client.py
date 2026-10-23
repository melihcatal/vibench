import os
from google.cloud import texttospeech

_tts_client = None

def get_tts_client() -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a Google Cloud TextToSpeechClient.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable implicitly.
    """
    global _tts_client
    if _tts_client is None:
        _tts_client = texttospeech.TextToSpeechClient()
    return _tts_client
