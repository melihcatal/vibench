import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    client = translate.Client()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    # or explicit credentials can be passed.
    # For local development, ensure you have authenticated with `gcloud auth application-default login`

    result = client.translate(text, target_language=target_language)
    return result['translatedText']
