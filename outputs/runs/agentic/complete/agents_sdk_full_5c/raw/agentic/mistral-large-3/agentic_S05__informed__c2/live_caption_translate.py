import os
from google.cloud import translate_v2 as translate

_translate_client = translate.Client()


def translate_caption(text: str, target_language: str = "es") -> str:
    if not text.strip():
        return ""
    result = _translate_client.translate(text, target_language=target_language)
    return result["translatedText"]