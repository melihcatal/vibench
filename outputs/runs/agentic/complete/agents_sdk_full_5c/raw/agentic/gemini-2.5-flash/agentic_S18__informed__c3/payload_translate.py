from google.cloud import translate_v2 as translate
import os

def translate_payload_text(text: str, target_language: str = "es") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']
