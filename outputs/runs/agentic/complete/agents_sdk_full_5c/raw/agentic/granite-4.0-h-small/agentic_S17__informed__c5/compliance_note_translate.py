import os
from google.cloud import translate_v2 as translate

from security_models import SignOrVerifyRequest

def compliance_note_translate(note: str, target_language: str = 'es') -> str:
    """Translates a compliance / encryption note into the requested language.

    Uses Google Cloud Translation API (Google Gemini Text Translation service).
    Returns the translated string.
    """
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result['translatedText']
