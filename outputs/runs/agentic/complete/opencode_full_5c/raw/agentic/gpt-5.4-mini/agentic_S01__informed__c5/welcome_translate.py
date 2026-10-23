import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_locale: str) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_locale.split("-")[0])
    return result["translatedText"]
