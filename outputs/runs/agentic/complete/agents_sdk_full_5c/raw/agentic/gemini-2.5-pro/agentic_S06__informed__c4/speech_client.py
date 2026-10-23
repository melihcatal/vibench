import os
from functools import lru_cache

from google.cloud import texttospeech


@lru_cache(maxsize=1)
def get_speech_client() -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a TextToSpeechClient.

    Authentication is handled implicitly by the Google Cloud client library
    using the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return texttospeech.TextToSpeechClient()
