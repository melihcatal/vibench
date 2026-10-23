import os

from google.cloud import translate_v2 as translate


def appeal_translate(text):
    client = translate.Client()
    result = client.translate(text, target_language="en")
    return result["translatedText"]
