import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> str:
    client = translate.Client()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file for authentication.

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
