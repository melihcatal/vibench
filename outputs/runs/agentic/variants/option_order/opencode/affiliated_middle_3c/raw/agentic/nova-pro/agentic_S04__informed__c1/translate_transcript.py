import os
from google.cloud import translate_v2 as translate


def translate_transcript(transcript):
    client = translate.Client()
    result = client.translate(transcript, target_language="es")
    return result["translatedText"]
