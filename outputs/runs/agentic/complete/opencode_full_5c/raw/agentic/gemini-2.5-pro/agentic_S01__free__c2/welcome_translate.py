import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str) -> str:
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
