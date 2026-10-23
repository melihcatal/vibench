from google.cloud import translate_v2 as translate
import os

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def welcome_translate(text, target_language):
    client = translate.Client(project=GOOGLE_CLOUD_PROJECT)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
