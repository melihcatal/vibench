import os
from translate_client import TranslationClient

def batch_translate(texts: list[str], source_lang: str, target_lang: str) -> list[str]:
    """Translate a list of strings while preserving order.

    Args:
        texts: list of source texts.
        source_lang: source language code.
        target_lang: target language code.

    Returns:
        List of translated texts in the same order.
    """
    client = TranslationClient()
    return client.batch_translate(texts, source_lang, target_lang)
