from google.cloud import translate_v2 as translate
import os

def translate_runbook_notes(text: str, target_language_code: str = 'en') -> str | None:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    Assumes GOOGLE_APPLICATION_CREDENTIALS are set up for authentication.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language_code
        )
        return result['translatedText']
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation API: {e}")
        return None
