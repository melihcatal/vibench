import os
from google.cloud import translate_v2 as translate


def translate_welcome_message(text: str, target_language: str) -> str:
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
