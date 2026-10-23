"""
multilingual_query_translate.py - Translate queries before multilingual embedding search.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Any

import deepl


DEEPL_TARGET_LANG = "EN"

_auth_key = os.environ.get("DEEPL_AUTH_KEY", "")


def _get_deepl_client() -> deepl.Translator:
    if not _auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL Translation API.")
    return deepl.Translator(_auth_key)


def translate_query(
    query: str,
    source_lang: str = "AUTO",
    target_lang: str = DEEPL_TARGET_LANG,
    formality: str | None = None,
) -> str:
    """Translate a search query to the target language via DeepL API.

    Enables multilingual embedding search by translating non-English queries
    into English (or another target language) before embedding with a monolingual model.

    Args:
        query: The input query text to translate.
        source_lang: Source language code (default: AUTO for auto-detection).
        target_lang: Target language code (default: EN).
        formality: Optional formality level ("more", "less", "default", "prefer_more", "prefer_less").

    Returns:
        Translated query text.
    """
    client = _get_deepl_client()

    kwargs: dict[str, Any] = {
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    if formality is not None:
        kwargs["formality"] = formality

    result = client.translate_text(query, **kwargs)
    return result.text


def translate_queries_batch(
    queries: list[str],
    source_lang: str = "AUTO",
    target_lang: str = DEEPL_TARGET_LANG,
) -> list[str]:
    """Translate multiple queries in a single DeepL API call.

    Args:
        queries: List of query strings to translate.
        source_lang: Source language code (default: AUTO).
        target_lang: Target language code (default: EN).

    Returns:
        List of translated query strings.
    """
    client = _get_deepl_client()

    results = client.translate_text(
        queries,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    return [r.text for r in results]


def prepare_multilingual_search(
    queries: list[str],
    source_languages: list[str] | None = None,
    target_language: str = DEEPL_TARGET_LANG,
) -> list[dict[str, str]]:
    """Translate queries and return structured search-ready objects.

    Each output dict contains the original query, translated query,
    and detected/source language for downstream embedding search.

    Args:
        queries: List of queries in various languages.
        source_languages: Optional list of source language codes (one per query).
        target_language: Target language for translation (default: EN).

    Returns:
        List of dicts with 'original', 'translated', and 'source_lang' keys.
    """
    if source_languages is None:
        source_languages = ["AUTO"] * len(queries)

    prepared: list[dict[str, str]] = []
    for query, src in zip(queries, source_languages):
        translated = translate_query(query, source_lang=src, target_lang=target_language)
        prepared.append({
            "original": query,
            "translated": translated,
            "source_lang": src,
            "target_lang": target_language,
        })
    return prepared


def main() -> None:
    multilingual_queries = [
        "¿Qué es el aprendizaje automático?",
        "Qu'est-ce que l'intelligence artificielle?",
        "Was ist maschinelles Lernen?",
        "機械学習とは何ですか？",
    ]

    results = prepare_multilingual_search(multilingual_queries)
    for item in results:
        print(f"Original ({item['source_lang']}): {item['original']}")
        print(f"  Translated ({item['target_lang']}): {item['translated']}")
        print()


if __name__ == "__main__":
    main()
