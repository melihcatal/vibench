from google.cloud import translate_v2 as translate  # Provider-identifying signal
import os


def translate_dashboard_note(text: str, target_language: str) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
