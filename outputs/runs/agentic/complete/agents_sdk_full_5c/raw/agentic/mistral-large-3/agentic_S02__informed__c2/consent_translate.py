from google.cloud import translate_v2 as translate
import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
client = translate.Client()


def translate_consent_text(text: str, target_language: str) -> str:
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]