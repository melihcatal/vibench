"""
appeal_translate.py - Translate appeal text for review.

Provider: DeepL API
  - SDK: deepl
  - Env: DEEPL_AUTH_KEY
  - API: api-free.deepl.com / api.deepl.com
"""

from __future__ import annotations

import os
from typing import Optional, List

import deepl


def get_deepl_client() -> deepl.Translator:
    """Create a DeepL translator using the DEEPL_AUTH_KEY environment variable."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    server_url = os.environ.get("DEEPL_SERVER_URL")
    if server_url:
        return deepl.Translator(auth_key, server_url=server_url)
    return deepl.Translator(auth_key)


def translate_appeal_text(
    appeal_text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate an appeal text for content moderation review using DeepL.

    Supported target languages include: EN, DE, FR, ES, IT, NL, PL, PT, RU, JA, ZH, etc.

    Args:
        appeal_text: The original appeal text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Optional source language code for better accuracy.
        client: Optional pre-configured DeepL translator.
        formality: Optional formality level ('more' or 'less').

    Returns:
        The translated appeal text.

    Raises:
        ValueError: If appeal_text is empty.
        deepl.DeepLException: If the translation API call fails.
    """
    if not appeal_text or not appeal_text.strip():
        raise ValueError("Appeal text must not be empty.")

    if client is None:
        client = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_lang,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    result = client.translate_text(appeal_text, **translate_kwargs)
    return result.text


def translate_appeal_batch(
    appeal_texts: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
    formality: Optional[str] = None,
) -> List[str]:
    """
    Translate a batch of appeal texts using DeepL.

    Args:
        appeal_texts: List of appeal texts to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.
        client: Optional pre-configured DeepL translator.
        formality: Optional formality level.

    Returns:
        List of translated texts.
    """
    if not appeal_texts:
        return []

    if client is None:
        client = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_lang,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    results = client.translate_text(appeal_texts, **translate_kwargs)

    if isinstance(results, list):
        return [r.text for r in results]
    return [results.text]


def detect_and_translate_appeal(
    appeal_text: str,
    target_lang: str = "EN",
    client: Optional[deepl.Translator] = None,
) -> dict:
    """
    Detect the source language and translate the appeal text.

    Args:
        appeal_text: The appeal text to process.
        target_lang: Target language code.
        client: Optional pre-configured DeepL translator.

    Returns:
        Dict with 'detected_source', 'translated_text', and 'original_text'.
    """
    if client is None:
        client = get_deepl_client()

    result = client.translate_text(
        appeal_text,
        target_lang=target_lang,
        source_lang=None,
    )

    return {
        "detected_source": result.detected_source_lang,
        "translated_text": result.text,
        "original_text": appeal_text,
    }
