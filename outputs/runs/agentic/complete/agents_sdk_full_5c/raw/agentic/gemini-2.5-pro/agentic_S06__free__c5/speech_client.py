from google.cloud import texttospeech
from functools import lru_cache

@lru_cache(maxsize=1)
def get_speech_client() -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a singleton TextToSpeechClient.
    
    Authentication is handled implicitly by the Google Cloud SDK,
    which checks for credentials in the environment.
    """
    return texttospeech.TextToSpeechClient()
