import os
from translate_client import TranslationClient

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate a single string using the configured provider.

    Args:
        text: the source text to translate.
        source_lang: source language code (e.g., \"en\").
        target_lang: target language code (e.g., \"fr\").

    Returns:
        Translated text.
    """
    client = TranslationClient()
    return client.translate(text, source_lang, target_lang)
