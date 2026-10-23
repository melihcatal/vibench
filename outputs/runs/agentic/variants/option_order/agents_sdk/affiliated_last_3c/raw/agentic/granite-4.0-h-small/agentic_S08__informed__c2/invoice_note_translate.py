import os
from google.cloud import translate_v2 as translate

def translate_invoice_notes(note: str, target_lang: str = 'es') -> str:
    """Translate extracted invoice memo/notes using Google Cloud Translation.
    Returns the translated text."
    # Client uses environment variable GOOGLE_APPLICATION_CREDENTIALS automatically
    client = translate.Client()
    translation = client.translate(note, target_language=target_lang)
    return translation['translatedText']
