import os
import deepl
from typing import List, Optional


def translate_query_for_search(
    query: str, target_lang: str = "EN-US", source_lang: Optional[str] = None
) -> str:
    """Translate queries before multilingual embedding search using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            query, target_lang=target_lang, source_lang=source_lang
        )
        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation failed: {e}")


def translate_queries_batch(
    queries: List[str], target_lang: str = "EN-US", source_lang: Optional[str] = None
) -> List[str]:
    """Translate a batch of queries using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        results = translator.translate_text(
            queries, target_lang=target_lang, source_lang=source_lang
        )
        return [result.text for result in results]
    except deepl.DeepLException as e:
        raise Exception(f"DeepL batch translation failed: {e}")


def detect_language(query: str) -> str:
    """Detect language of a query using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            query[:50],  # Use first 50 chars for detection
            target_lang="EN-US",
        )
        return result.detected_source_lang
    except deepl.DeepLException as e:
        raise Exception(f"DeepL language detection failed: {e}")
