import os
from google.cloud import translate_v2 as translate


def translate_transcript(text):
    translate_client = translate.Client(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    result = translate_client.translate(text, target_language="es")
    return result["translatedText"]
