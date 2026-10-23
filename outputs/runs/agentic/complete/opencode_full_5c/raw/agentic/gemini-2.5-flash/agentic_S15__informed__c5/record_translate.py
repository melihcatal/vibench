import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_record_field(text: str, target_language: str = "es") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication.
    # No explicit key is passed if GOOGLE_APPLICATION_CREDENTIALS is configured.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
