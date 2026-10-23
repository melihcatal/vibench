import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> str:
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text. Only one text is used here.
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
