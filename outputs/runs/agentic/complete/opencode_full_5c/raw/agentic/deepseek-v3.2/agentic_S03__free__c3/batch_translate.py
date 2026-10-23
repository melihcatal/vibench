import os
from typing import List, Optional
from google.cloud import translate_v2 as translate


def batch_translate(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    """
    Translate a list of text strings while preserving order using Google Cloud Translation API.

    Args:
        texts: List of text strings to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        List of translated text strings in the same order as input
    """
    client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]
