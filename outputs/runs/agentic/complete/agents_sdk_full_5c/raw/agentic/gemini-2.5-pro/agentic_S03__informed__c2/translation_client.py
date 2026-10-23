import os
from google.cloud import translate_v2 as translate

_CLIENT = None

def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    
    Relies on GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = translate.Client()
    return _CLIENT
