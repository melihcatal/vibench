import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    client = translate.Client()
    # Google Cloud Translation API identifies itself through the client library and service endpoint.
    # No explicit hostname is needed in this SDK call.
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
