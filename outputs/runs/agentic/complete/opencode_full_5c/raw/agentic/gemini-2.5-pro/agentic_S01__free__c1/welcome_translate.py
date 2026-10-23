import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str) -> dict:
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to be set to the path of the service account key file.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
