"""
Translates a list of strings while preserving order.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from typing import List, Optional

from translation_client import get_client
from translation_models import TranslationResponse, TranslationResult


def batch_translate(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResponse:
    """
    Translate a list of strings, preserving the original order.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code (optional; DeepL auto-detects if omitted).
        formality: Formality level ('prefer_more' or 'prefer_less'; optional).

    Returns:
        TranslationResponse containing ordered TranslationResult objects.
    """
    if not texts:
        return TranslationResponse()

    client = get_client()
    response = client.translate_batch(
        texts=texts,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )
    return response


def batch_translate_with_callbacks(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    chunk_size: int = 50,
) -> List[TranslationResult]:
    """
    Translate a large list in chunks, preserving order across chunks.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional).
        formality: Formality level (optional).
        chunk_size: Maximum number of texts per API call.

    Returns:
        Ordered list of TranslationResult objects.
    """
    all_results: List[TranslationResult] = []
    client = get_client()

    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i + chunk_size]
        response = client.translate_batch(
            texts=chunk,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
        )
        all_results.extend(response.results)

    return all_results


if __name__ == "__main__":
    texts = ["Hello", "Good morning", "See you later"]
    response = batch_translate(texts, target_lang="DE")
    for result in response.results:
        print(f"{result.text}")
