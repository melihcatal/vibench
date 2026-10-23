"""Translate queries before multilingual embedding search using DeepL API.

Uses the DeepL translation API to translate search queries into a target language
before embedding-based semantic search is performed.
"""

import os
from typing import List, Dict, Optional

import deepl


def get_deepl_client() -> deepl.Translator:
    """Create a DeepL translator client from environment variables."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(auth_key)


def translate_query(
    query: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> str:
    """Translate a single search query to the target language via DeepL.

    Args:
        query: Original query text in any language.
        target_lang: Target language code (e.g., 'EN', 'ES', 'FR', 'DE', 'JA').
        source_lang: Optional source language code for more accurate translation.
        client: Pre-created DeepL translator client.

    Returns:
        Translated query string.
    """
    translator = client or get_deepl_client()

    params: Dict = {
        "target_lang": target_lang,
    }
    if source_lang:
        params["source_lang"] = source_lang

    result = translator.translate_text(query, **params)
    return result.text


def translate_queries_batch(
    queries: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> List[Dict[str, str]]:
    """Translate multiple queries for multilingual embedding search via DeepL.

    Args:
        queries: List of query strings to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.
        client: Pre-created DeepL translator client.

    Returns:
        List of dicts with 'original', 'translated', and 'target_lang' keys.
    """
    translator = client or get_deepl_client()

    params: Dict = {
        "target_lang": target_lang,
    }
    if source_lang:
        params["source_lang"] = source_lang

    translated = translator.translate_text(queries, **params)

    results = []
    for orig, trans in zip(queries, translated):
        results.append({
            "original": orig,
            "translated": trans.text,
            "target_lang": target_lang,
        })

    return results


def prepare_multilingual_search(
    query: str,
    target_languages: List[str],
    source_lang: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Prepare a query for multilingual embedding search by translating to multiple languages.

    Translates the query to each target language so embeddings can be computed
    in each language's vector space for cross-lingual retrieval.

    Args:
        query: Original search query.
        target_languages: List of target language codes (e.g., ['EN', 'ES', 'FR']).
        source_lang: Optional source language code.

    Returns:
        List of dicts with 'original', 'translated', and 'language' keys.
    """
    translator = get_deepl_client()
    results = []

    for lang in target_languages:
        translated = translate_query(
            query,
            target_lang=lang,
            source_lang=source_lang,
            client=translator,
        )
        results.append({
            "original": query,
            "translated": translated,
            "language": lang,
        })

    return results


def main():
    sample_queries = [
        "¿Cómo funciona el aprendizaje profundo?",
        "Comment fonctionne l'apprentissage profond?",
        "How does deep learning work?",
    ]
    target_lang = os.environ.get("TRANSLATE_TARGET_LANG", "EN")

    try:
        results = translate_queries_batch(sample_queries, target_lang=target_lang)
        print(f"DeepL Translation Results -> {target_lang}:")
        for r in results:
            print(f"  [{r['target_lang']}] {r['original']} -> {r['translated']}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set DEEPL_AUTH_KEY to use this module.")


if __name__ == "__main__":
    main()
