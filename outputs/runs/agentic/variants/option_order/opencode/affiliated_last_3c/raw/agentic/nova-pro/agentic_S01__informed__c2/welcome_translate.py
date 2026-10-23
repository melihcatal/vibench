import os
from google.cloud import translate_v2 as translate

# Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

translate_client = translate.Client()


def welcome_translate(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
