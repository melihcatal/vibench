import json
from google.cloud import translate_v2 as translate

def translate_invoice_note(note: str, target_lang: str = 'es') -> str:
    """Translate an invoice note or description to a target language using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(note, target_language=target_lang)
    return result['translatedText']
