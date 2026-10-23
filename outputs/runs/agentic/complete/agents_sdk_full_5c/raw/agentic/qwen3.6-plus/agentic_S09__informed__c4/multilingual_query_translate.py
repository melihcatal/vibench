"""
Translate queries before multilingual embedding search using DeepL API.

Translates user queries into a target language before embedding,
enabling multilingual semantic search over a monolingual document corpus.
Uses the DeepL API with the deepl SDK.

Requires DEEPL_AUTH_KEY environment variable or explicit auth_key parameter.
"""

from typing import List, Optional

import deepl

DEEPL_TARGET_LANG = "EN"
DEEPL_SOURCE_LANG_AUTO = None


def get_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    """
    Create and return an authenticated DeepL translator.

    Args:
        auth_key: DeepL authentication key. Falls back to DEEPL_AUTH_KEY env var.

    Returns:
        Configured deepl.Translator instance.
    """
    key = auth_key or __import__("os").environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DeepL auth key not provided and DEEPL_AUTH_KEY not set")
    return deepl.Translator(key)


def translate_query(
    query: str,
    target_language: str = DEEPL_TARGET_LANG,
    source_language: Optional[str] = DEEPL_SOURCE_LANG_AUTO,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> str:
    """
    Translate a single search query using DeepL API.

    Args:
        query: The input query text to translate.
        target_language: Target language code (e.g., 'EN', 'DE', 'ES', 'FR', 'JA').
        source_language: Source language code, or None for auto-detect.
        auth_key: DeepL auth key. Falls back to DEEPL_AUTH_KEY env var.
        translator: Pre-configured deepl.Translator (optional).

    Returns:
        Translated query text string.
    """
    if translator is None:
        translator = get_deepl_translator(auth_key)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    result = translator.translate_text(query, **kwargs)
    return result.text


def translate_queries_batch(
    queries: List[str],
    target_language: str = DEEPL_TARGET_LANG,
    source_language: Optional[str] = DEEPL_SOURCE_LANG_AUTO,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> List[str]:
    """
    Translate a list of search queries using DeepL API.

    Args:
        queries: List of input query texts to translate.
        target_language: Target language code.
        source_language: Source language code, or None for auto-detect.
        auth_key: DeepL auth key.
        translator: Optional pre-built deepl.Translator.

    Returns:
        List of translated query strings in the same order as input.
    """
    if not queries:
        return []

    if translator is None:
        translator = get_deepl_translator(auth_key)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    results = translator.translate_text(queries, **kwargs)
    return [r.text for r in results]


def prepare_search_queries(
    queries: List[str],
    target_language: str = DEEPL_TARGET_LANG,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> List[str]:
    """
    Prepare queries for multilingual embedding search via translation.

    Translates each query into the target language so they can be
    embedded using the same model as the target-language document corpus.

    Args:
        queries: Original query texts in various source languages.
        target_language: Language code for the document corpus.
        auth_key: DeepL auth key.
        translator: Optional pre-built translator.

    Returns:
        List of translated queries ready for embedding.
    """
    return translate_queries_batch(
        queries=queries,
        target_language=target_language,
        auth_key=auth_key,
        translator=translator,
    )
