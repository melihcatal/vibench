import os
from translation_client import TranslationClient

def translate_text(text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate a single text string using the configured provider."""    client = TranslationClient()
    response = client.translate(text, source_lang, target_lang)
    return response['translatedText']
