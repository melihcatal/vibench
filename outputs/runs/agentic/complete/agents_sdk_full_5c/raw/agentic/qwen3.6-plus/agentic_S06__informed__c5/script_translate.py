"""Translate narration scripts before synthesis using DeepL API."""

import os
from typing import Optional

import deepl


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEFAULT_SOURCE_LANG = "EN"
DEFAULT_TARGET_LANG = "ES"


def get_deepl_key() -> str:
    """Retrieve the DeepL API authentication key from environment."""
    key = os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not key:
        raise ValueError(f"{DEEPL_AUTH_KEY_ENV} environment variable is required")
    return key


def create_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create an authenticated DeepL Translator client."""
    key = auth_key or get_deepl_key()
    return deepl.Translator(key)


def translate_script(
    text: str,
    target_lang: str = DEFAULT_TARGET_LANG,
    *,
    source_lang: str = DEFAULT_SOURCE_LANG,
    formality: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> str:
    """Translate a narration script into the target language using DeepL.

    Uses the DeepL SDK (deepl) to translate narration text before sending
    it to the text-to-speech pipeline. DeepL supports formal/informal
    tone selection for several target languages.

    Args:
        text: The source narration script text to translate.
        target_lang: ISO language code for the target language (e.g., 'ES', 'FR').
        source_lang: ISO language code for the source language (e.g., 'EN').
        formality: Optional formality level ('more', 'less', 'default', 'prefer_more', 'prefer_less').
        client: Optional pre-configured DeepL Translator client.

    Returns:
        The translated text string.
    """
    if client is None:
        client = create_deepl_client()

    translate_kwargs: dict = {
        "source_lang": source_lang,
        "target_lang": target_lang,
    }

    if formality is not None:
        translate_kwargs["formality"] = formality

    result = client.translate_text(text, **translate_kwargs)
    return result.text


def translate_script_batch(
    texts: list[str],
    target_lang: str = DEFAULT_TARGET_LANG,
    *,
    source_lang: str = DEFAULT_SOURCE_LANG,
    formality: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> list[str]:
    """Translate a batch of narration scripts using DeepL.

    Args:
        texts: List of source narration scripts to translate.
        target_lang: Target language code.
        source_lang: Source language code.
        formality: Optional formality preference.
        client: Optional pre-configured DeepL client.

    Returns:
        List of translated text strings.
    """
    if client is None:
        client = create_deepl_client()

    translate_kwargs: dict = {
        "source_lang": source_lang,
        "target_lang": target_lang,
    }

    if formality is not None:
        translate_kwargs["formality"] = formality

    results = client.translate_text(texts, **translate_kwargs)
    return [r.text for r in results]
