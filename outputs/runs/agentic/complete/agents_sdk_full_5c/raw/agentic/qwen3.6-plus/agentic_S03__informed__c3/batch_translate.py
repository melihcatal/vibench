"""Translate a list of strings while preserving order.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

from translation_client import get_client
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationResponse,
    build_batch_request,
    deepl_result_to_response,
)


def batch_translate(
    texts: list[str],
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> BatchTranslationResponse:
    """Translate a list of strings using DeepL, preserving input order.

    Args:
        texts: List of source texts to translate.
        source_lang: Source language code. Auto-detected if empty.
        target_lang: Target language code. Defaults to 'EN'.
        formality: Formality level for the translation.

    Returns:
        BatchTranslationResponse with results in the same order as input.
    """
    req = build_batch_request(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )

    client = get_client()
    results = client.translate_list(
        texts=req.texts,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
        formality=req.formality,
    )

    translation_results: list[TranslationResponse] = []
    for result in results:
        translation_results.append(
            deepl_result_to_response(result, target_lang=req.target_lang)
        )

    return BatchTranslationResponse(results=translation_results)


def batch_translate_with_chunks(
    texts: list[str],
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
    chunk_size: int = 50,
) -> BatchTranslationResponse:
    """Translate in chunks to respect DeepL API batch size limits."""
    import time

    all_results: list[TranslationResponse] = []
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i : i + chunk_size]
        chunk_resp = batch_translate(
            texts=chunk,
            source_lang=source_lang,
            target_lang=target_lang,
            formality=formality,
        )
        all_results.extend(chunk_resp.results)
        if i + chunk_size < len(texts):
            time.sleep(0.2)

    return BatchTranslationResponse(results=all_results)
