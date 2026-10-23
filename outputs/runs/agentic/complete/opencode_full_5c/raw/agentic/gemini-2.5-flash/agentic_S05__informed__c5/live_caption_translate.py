import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
