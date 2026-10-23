import os
from google.cloud import translate_v2 as translate


def appeal_translate(text: str, target_language: str = "en") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or explicit credentials provided.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
