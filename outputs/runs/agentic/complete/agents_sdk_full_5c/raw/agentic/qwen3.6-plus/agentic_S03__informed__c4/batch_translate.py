"""
Translate a list of strings while preserving order.

Provider: DeepL Translation API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

import deepl

from translation_client import create_translation_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_source_language,
)


def batch_translate(
    texts: list[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> TranslationResponse:
    """
    Translate a list of text strings, preserving the order of results.

    DeepL's translate_text method accepts a list of strings and returns
    results in the same order.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'JA').
            Supports regional variants: 'EN-US', 'EN-GB', 'PT-BR', 'PT-PT'.
        source_lang: Source language code, or None for auto-detection.
        formality: Controls formality level for supported languages.
        preserve_formatting: Whether to preserve formatting.
        client: Optional pre-created DeepL Translator client.

    Returns:
        TranslationResponse with all translated strings in order.

    Raises:
        deepl.DeepLException: If the DeepL API request fails.
        ValueError: If the request is invalid.
    """
    if not texts:
        return TranslationResponse(translations=[])

    if client is None:
        client = create_translation_client()

    normalized_source = normalize_source_language(source_lang)
    normalized_target = target_lang.strip().upper()

    translate_kwargs: dict = {
        "target_lang": normalized_target,
        "preserve_formatting": preserve_formatting,
    }

    if normalized_source is not None:
        translate_kwargs["source_lang"] = normalized_source

    if formality is not None:
        translate_kwargs["formality"] = formality

    raw_results = client.translate_text(texts, **translate_kwargs)

    translations: list[TranslationResult] = []
    char_count = 0

    for result in raw_results:
        translations.append(TranslationResult(
            text=result.text,
            detected_source_lang=getattr(result, "detected_source_lang", None),
            model_info=None,
        ))
        char_count += len(result.text)

    return TranslationResponse(
        translations=translations,
        character_count=char_count,
    )


def batch_translate_chunks(
    texts: list[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    chunk_size: int = 50,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> TranslationResponse:
    """
    Translate a large list of texts in chunks to handle API limits.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        source_lang: Source language code, or None for auto-detection.
        chunk_size: Maximum texts per API call (DeepL allows up to 50).
        formality: Controls formality level.
        preserve_formatting: Whether to preserve formatting.
        client: Optional pre-created DeepL Translator client.

    Returns:
        TranslationResponse with all translated strings in order.
    """
    if not texts:
        return TranslationResponse(translations=[])

    all_translations: list[TranslationResult] = []
    total_chars = 0

    for i in range(0, len(texts), chunk_size):
        chunk = texts[i : i + chunk_size]
        chunk_response = batch_translate(
            texts=chunk,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
            preserve_formatting=preserve_formatting,
            client=client,
        )
        all_translations.extend(chunk_response.translations)
        total_chars += chunk_response.character_count

    return TranslationResponse(
        translations=all_translations,
        character_count=total_chars,
    )


if __name__ == "__main__":
    items = [
        "Hello, how are you?",
        "Good morning!",
        "Where is the nearest restaurant?",
    ]
    response = batch_translate(items, target_lang="FR")
    for t in response.translations:
        print(t.text)
