import os
from google.cloud import translate_v2 as translate


def translate_payload_text(text: str, target_language: str = "en") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]
    print(f"Translated text: {translated_text}")
    return translated_text
