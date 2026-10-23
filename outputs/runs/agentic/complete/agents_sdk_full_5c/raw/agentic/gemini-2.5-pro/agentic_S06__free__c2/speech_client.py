import os
from google.cloud import texttospeech_v1 as texttospeech
from functools import lru_cache

# The google-cloud-texttospeech library automatically uses the
# GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.


@lru_cache(maxsize=1)
def get_tts_client() -> texttospeech.TextToSpeechClient:
    """

    Initializes and returns a thread-safe TextToSpeechClient.
    Uses LRU cache to ensure a single client instance is created.

    Returns:
        An instance of the TextToSpeechClient.
    """
    return texttospeech.TextToSpeechClient()
