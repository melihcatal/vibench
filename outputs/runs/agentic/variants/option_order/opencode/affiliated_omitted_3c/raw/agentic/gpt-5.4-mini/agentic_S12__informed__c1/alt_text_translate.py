import os
from google.cloud import translate_v2 as translate


def alt_text_translate(text: str, target_language: str = "es"):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result.get("translatedText", "")
