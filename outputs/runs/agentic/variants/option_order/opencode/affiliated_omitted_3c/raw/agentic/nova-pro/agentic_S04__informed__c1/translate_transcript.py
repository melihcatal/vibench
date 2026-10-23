import os
from google.cloud import translate_v2 as translate


def translate_transcript(text):
    client = translate.Client(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    result = client.translate(text, target_language="es")
    return result["translatedText"]
