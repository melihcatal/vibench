from google.cloud import translate_v2 as translate
import os


def record_translate(text: str, target_language: str):
    translate_client = translate.Client()

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable needs to be set
    # to a path to a service account key file.

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
