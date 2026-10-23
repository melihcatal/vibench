import os
from google.cloud import translate_v2 as translate

def appeal_translate(text: str, target_language: str = "en") -> str:
    """
    Translate appeal text for review using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up (e.g., via environment variable pointing to a service account key file).
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    client = translate.Client()

    result = client.translate(text, target_language=target_language)
    return result['translatedText']

