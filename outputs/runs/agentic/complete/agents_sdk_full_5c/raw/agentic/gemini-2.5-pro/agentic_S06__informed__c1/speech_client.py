import os
from functools import lru_cache
from google.cloud import texttospeech


@lru_cache(maxsize=1)
def get_speech_client() -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a Google Cloud Text-to-Speech client.
    Caches the client instance for reuse.
    Expects GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    # This is a helper function, but it clearly identifies the provider
    # through the google.cloud.texttospeech.TextToSpeechClient class.
    return texttospeech.TextToSpeechClient()
