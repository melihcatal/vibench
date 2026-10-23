from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str = "en") -> str:
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable is set or configure application default credentials.
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
