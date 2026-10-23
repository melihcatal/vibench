from google.cloud import translate_v2 as translate
from typing import List
import os

# Provider: Google Cloud Translation (v2)
# Model: google/cloud-translate-v2


def batch_translate(
    texts: List[str], target_language: str, source_language: str = None
) -> List[str]:
    """
    Translates a list of strings while preserving order using Google Cloud Translation.

    Args:
        texts: The list of texts to translate.
        target_language: The target language code (e.g., 'es', 'fr').
        source_language: The source language code (optional, e.g., 'en').

    Returns:
        A list of translated texts in the same order as the input.
    """
    if not texts:
        return texts

    client = translate.Client()
    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [result["translatedText"] for result in results]
