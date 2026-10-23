import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates a given text into the target language using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    translate_client = translate.Client()

    # Target language must be provided as an ISO 639-1 code
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
