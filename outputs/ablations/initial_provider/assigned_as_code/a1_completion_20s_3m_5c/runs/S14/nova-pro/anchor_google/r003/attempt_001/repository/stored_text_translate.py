import os
from google.cloud import translate_v2 as translate


def stored_text_translate(text, target_language, config=None):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {"translated_text": result["translatedText"]}