import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text to a target language using Google Cloud Translate.
    """

    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    # to a service account JSON file with Translate API permissions.

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
