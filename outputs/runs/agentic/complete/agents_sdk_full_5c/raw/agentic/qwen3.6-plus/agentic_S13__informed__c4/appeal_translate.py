"""
Translate appeal text for moderation review.
Provider: DeepL API
"""

import os
from typing import Optional, List, Dict

import deepl


def _get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(auth_key)


def translate_appeal(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate an appeal text using the DeepL Translation API.

    Args:
        text: The appeal text to translate.
        target_lang: Target language code (e.g. 'EN', 'ES', 'FR', 'DE', 'JA').
        source_lang: Source language code. If None, DeepL auto-detects.
        formality: Formality preference ('more', 'less', or 'default').

    Returns:
        Translated text string.
    """
    client = _get_deepl_client()

    kwargs: Dict = {}
    if source_lang:
        kwargs["source_lang"] = source_lang
    if formality:
        kwargs["formality"] = formality

    result = client.translate_text(text, target_lang=target_lang, **kwargs)
    return result.text


def translate_appeal_batch(
    texts: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple appeal texts using DeepL API.

    Args:
        texts: List of appeal texts to translate.
        target_lang: Target language code.
        source_lang: Source language code. Auto-detected if None.
        formality: Formality preference.

    Returns:
        List of translated text strings.
    """
    client = _get_deepl_client()

    kwargs: Dict = {}
    if source_lang:
        kwargs["source_lang"] = source_lang
    if formality:
        kwargs["formality"] = formality

    results = client.translate_text(texts, target_lang=target_lang, **kwargs)
    return [r.text for r in results]


def translate_appeal_for_review(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    include_original: bool = True,
) -> Dict:
    """
    Translate an appeal and return structured data for review.

    Args:
        text: The appeal text to translate.
        target_lang: Target language code.
        source_lang: Source language code. Auto-detected if None.
        include_original: Whether to include the original text in output.

    Returns:
        Dict with translated text and metadata.
    """
    translated = translate_appeal(
        text, target_lang=target_lang, source_lang=source_lang
    )

    result: Dict = {"translated_text": translated, "target_lang": target_lang}

    if include_original:
        result["original_text"] = text
        result["original_source"] = source_lang or "auto-detected"

    return result
