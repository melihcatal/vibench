import os
from google.cloud import translate_v2 as translate

# NOTE: GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication


def translate_compliance_note(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()
    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]
