import os
from typing import List, Optional
from translation_client import TranslationClient


def batch_translate(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    """
    Translate a list of strings while preserving order.

    Args:
        texts: List of text strings to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        List of translated text strings in same order as input
    """
    client = TranslationClient()

    # Use Google Cloud Translation API for batch translation
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if source_language:
        results = translate_client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = translate_client.translate(texts, target_language=target_language)

    # Extract translated texts preserving order
    translated_texts = [result["translatedText"] for result in results]
    return translated_texts
