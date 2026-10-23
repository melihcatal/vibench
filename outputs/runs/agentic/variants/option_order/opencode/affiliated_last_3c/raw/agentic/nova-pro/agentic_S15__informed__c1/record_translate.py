import os
from google.cloud import translate_v2 as translate


def record_translate(text, target_language):
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation["translatedText"]
