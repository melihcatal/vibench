import os
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

translate_client = translate.Client()


def translate_description(description, target_language="es"):
    result = translate_client.translate(description, target_language=target_language)
    return result["translatedText"]
