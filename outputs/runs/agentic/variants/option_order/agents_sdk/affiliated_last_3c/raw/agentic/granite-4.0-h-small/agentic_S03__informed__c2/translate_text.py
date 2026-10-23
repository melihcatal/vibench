import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(source_text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translates a single text string using the configured provider.
    """
    client = get_translation_client()
    request = TranslationRequest(text=source_text, source_lang=source_lang, target_lang=target_lang)
    response: TranslationResponse = client.translate(request)
    return response.translated_text
