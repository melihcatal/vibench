import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a list of concurrent translations.
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
