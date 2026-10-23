import os
from google.cloud import translate_v2 as translate


def translate_note(text: str, target_language: str) -> str:
    """
    Translates dashboard or metric notes to a target locale using Google Cloud Translation.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
