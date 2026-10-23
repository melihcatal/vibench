import os
from google.cloud import translate_v2 as translate


def translate_script(script, target_language):
    client = translate.Client()
    result = client.translate(script, target_language=target_language)
    return result["translatedText"]
