import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(texts: list[str], source_lang: str = 'en', target_lang: str = 'es') -> list[str]:
    """Translates a list of strings while preserving order using the configured provider.
    """
    client = get_translation_client()
    requests = [TranslationRequest(text=t, source_lang=source_lang, target_lang=target_lang) for t in texts]
    responses = client.translate_batch(requests)
    return [resp.translated_text for resp in responses]
