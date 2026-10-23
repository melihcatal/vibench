from google.cloud import translate_v2 as translate
import os

def translate_invoice_note(note: str, target_language: str = 'en-US') -> str:
    """Translate invoice note or description."""
    client = translate.Client()
    if not note.strip():
        return note
    result = client.translate(
        note,
        target_language=target_language,
        format_='text'
    )
    return result['translatedText']
