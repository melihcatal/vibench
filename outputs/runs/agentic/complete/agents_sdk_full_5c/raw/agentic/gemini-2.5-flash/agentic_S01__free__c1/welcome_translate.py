from google.cloud import translate_v2 as translate
import os

def welcome_translate(text: str, target_language: str) -> str:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set
    # Or provide project_id explicitly
    translate_client = translate.Client()

    # Target language must be an ISO 639-1 code
    # For example, 'fr' for French, 'es' for Spanish
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
