from google.cloud import translate_v2 as translate
import os

def translate_dashboard_note(text: str, target_language: str = 'es') -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
