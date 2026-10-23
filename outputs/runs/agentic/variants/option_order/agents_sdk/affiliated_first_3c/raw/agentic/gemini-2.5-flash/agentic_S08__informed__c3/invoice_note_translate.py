import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text. But for single note, it's simpler.
    result = translate_client.translate(text, target_language=target_language)

    # Google Cloud Translation identifies itself via the client library and implicitly via GOOGLE_APPLICATION_CREDENTIALS
    # For debugging, you might print result['detectedSourceLanguage']
    return result['translatedText']
