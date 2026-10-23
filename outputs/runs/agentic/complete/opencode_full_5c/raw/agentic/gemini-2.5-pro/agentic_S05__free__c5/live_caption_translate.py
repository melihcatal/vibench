import os
from google.cloud import translate_v2 as translate


def translate_live_caption(text: str, target_language: str = "fr"):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
