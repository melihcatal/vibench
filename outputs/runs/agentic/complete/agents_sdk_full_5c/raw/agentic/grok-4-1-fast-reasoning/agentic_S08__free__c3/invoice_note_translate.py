from google.cloud import translate_v2 as translate
import os

def invoice_note_translate(text: str, target_language: str = 'en') -> str:
    client = translate.Client()
    if isinstance(text, dict):
        text = text.get('value', '')
    result = client.translate(text, target_language=target_language)
    return result['translatedText']