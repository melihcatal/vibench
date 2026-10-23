import os
from google.cloud import translate_v2 as translate


def translate_alt_text(text: str, target_language: str = "es") -> str:
    translate_client = (
        translate.Client()
    )  # GOOGLE_APPLICATION_CREDENTIALS should be set

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
