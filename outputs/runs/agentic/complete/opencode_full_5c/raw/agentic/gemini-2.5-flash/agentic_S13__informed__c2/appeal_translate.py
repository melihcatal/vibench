import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    client = translate.Client()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or authentication configured otherwise.

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
