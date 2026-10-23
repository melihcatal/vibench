import os
from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str = "en") -> str:
    """Translate a narration script using Google Cloud Translation API.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]