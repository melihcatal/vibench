import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str) -> str:
    """
    Translates the given text to the target language.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
