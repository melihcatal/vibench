import os
from google.cloud import translate_v2 as translate

client = translate.Client(key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def translate_transcript(text, target_language):
    return client.translate(text, target_language=target_language)["translatedText"]
