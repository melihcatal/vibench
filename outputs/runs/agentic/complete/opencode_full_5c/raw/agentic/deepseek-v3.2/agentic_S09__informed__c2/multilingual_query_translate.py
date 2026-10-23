import os
from typing import List, Optional
import deepl


def translate_query(
    query: str, target_lang: str = "EN-US", source_lang: Optional[str] = None
) -> str:
    """
    Translate query text using DeepL API.

    Args:
        query: Query text to translate
        target_lang: Target language code (e.g., "EN-US", "DE", "FR")
        source_lang: Source language code (optional, auto-detected if None)

    Returns:
        str: Translated query

    Raises:
        ValueError: If DEEPL_AUTH_KEY is not set
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        query, target_lang=target_lang, source_lang=source_lang
    )

    return result.text


def translate_queries_batch(
    queries: List[str], target_lang: str = "EN-US", source_lang: Optional[str] = None
) -> List[str]:
    """
    Translate multiple queries using DeepL API.

    Args:
        queries: List of query texts to translate
        target_lang: Target language code
        source_lang: Source language code (optional)

    Returns:
        List[str]: List of translated queries
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    results = translator.translate_text(
        queries, target_lang=target_lang, source_lang=source_lang
    )

    return [result.text for result in results]


def detect_language(text: str) -> str:
    """
    Detect language of text using DeepL API.

    Args:
        text: Text to analyze

    Returns:
        str: Detected language code
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text,
        target_lang="EN-US",  # Target doesn't matter for detection
        source_lang=None,  # Auto-detect
    )

    return result.detected_source_lang
