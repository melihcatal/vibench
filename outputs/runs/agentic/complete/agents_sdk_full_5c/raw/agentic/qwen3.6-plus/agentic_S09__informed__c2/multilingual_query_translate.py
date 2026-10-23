"""
Later-step: Translate queries before multilingual embedding search.
Provider: DeepL API via deepl SDK.
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List, Optional

import deepl


def get_deepl_client(
    auth_key: Optional[str] = None,
    server_url: Optional[str] = None,
) -> deepl.Translator:
    """Create a DeepL translator client."""
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    kwargs: dict = {"auth_key": key}
    if server_url:
        kwargs["server_url"] = server_url
    return deepl.Translator(**kwargs)


def translate_queries(
    queries: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[str]:
    """Translate a list of queries to a target language using DeepL API.

    DeepL supports high-quality translation across 30+ languages, making it
    suitable for preparing queries before multilingual semantic search.

    Args:
        queries: List of query strings to translate.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'JA', 'ZH').
        source_lang: Optional source language code for better accuracy.
        auth_key: Optional override for DEEPL_AUTH_KEY.

    Returns:
        List of translated query strings.
    """
    translator = get_deepl_client(auth_key=auth_key)

    kwargs: dict = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    results: List[str] = []
    for query in queries:
        translated = translator.translate_text(query, **kwargs)
        results.append(translated.text)

    return results


def translate_and_prepare_for_search(
    query: str,
    target_lang: str = "EN",
    auth_key: Optional[str] = None,
) -> dict:
    """Translate a single query and return metadata for embedding search.

    Args:
        query: The original query text.
        target_lang: Target language for translation.
        auth_key: Optional DeepL auth key.

    Returns:
        Dict with original query, translated query, and language info.
    """
    translated_list = translate_queries([query], target_lang=target_lang, auth_key=auth_key)
    return {
        "original": query,
        "translated": translated_list[0],
        "target_lang": target_lang,
    }


if __name__ == "__main__":
    # Requires DEEPL_AUTH_KEY
    queries = [
        "Comment fonctionne la recherche sémantique?",
        "¿Qué es un vector de incrustación?",
        "嵌入向量是什么？",
    ]
    # translated = translate_queries(queries, target_lang="EN-US")
    # print(translated)
    print("Configure DEEPL_AUTH_KEY to run.")
