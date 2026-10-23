import os
from translation_client import TranslationClient

def batch_translate(texts: list[str], source_lang: str = 'en', target_lang: str = 'es') -> list[str]:
    """Translate a list of strings while preserving order."""    client = TranslationClient()
    responses = client.translate_batch(texts, source_lang, target_lang)
    return [r['translatedText'] for r in responses]
