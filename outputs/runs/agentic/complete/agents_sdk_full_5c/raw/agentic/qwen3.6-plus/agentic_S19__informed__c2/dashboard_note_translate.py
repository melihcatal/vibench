"""
Translate metric or dashboard notes for another locale using DeepL API.

Provides translation of dashboard annotations, metric descriptions,
and monitoring notes between languages.
Provider: DeepL (DEEPL_AUTH_KEY).
"""

import os
from typing import Optional

import deepl

DEEPL_TARGET_LANG_DEFAULT = "EN"


def _get_deepl_client() -> deepl.Translator:
    """Create an authenticated DeepL translator client."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(auth_key)


def translate_dashboard_note(
    note_text: str,
    target_lang: str = DEEPL_TARGET_LANG_DEFAULT,
    source_lang: Optional[str] = None,
) -> str:
    """
    Translate a single dashboard note using DeepL API.

    Args:
        note_text: The note text to translate.
        target_lang: Target language code (e.g., "EN", "DE", "JA", "ES").
        source_lang: Optional source language code for better accuracy.

    Returns:
        Translated text string.
    """
    translator = _get_deepl_client()

    kwargs: dict = {"target_lang": target_lang.upper()}
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()

    result = translator.translate_text(note_text, **kwargs)
    return result.text


def translate_metric_description(
    metric_name: str,
    description: str,
    target_lang: str = DEEPL_TARGET_LANG_DEFAULT,
) -> dict[str, str]:
    """
    Translate a metric description, returning original and translated text.

    Args:
        metric_name: The metric name (unchanged).
        description: Description text to translate.
        target_lang: Target language code.

    Returns:
        Dict with metric_name, original, and translated description.
    """
    translator = _get_deepl_client()

    result = translator.translate_text(
        description,
        target_lang=target_lang.upper(),
    )

    return {
        "metric": metric_name,
        "original": description,
        "translated": result.text,
        "target_language": target_lang.upper(),
    }


def translate_dashboard_notes_batch(
    notes: list[str],
    target_lang: str = DEEPL_TARGET_LANG_DEFAULT,
    source_lang: Optional[str] = None,
) -> list[str]:
    """
    Translate a batch of dashboard notes using DeepL API.

    Uses DeepL's batch translation for efficiency.

    Args:
        notes: List of note texts to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.

    Returns:
        List of translated texts.
    """
    translator = _get_deepl_client()

    kwargs: dict = {"target_lang": target_lang.upper()}
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()

    texts = translator.translate_text(notes, **kwargs)
    return [t.text for t in texts]


def translate_with_formality(
    note_text: str,
    target_lang: str = DEEPL_TARGET_LANG_DEFAULT,
    formality: str = "default",
) -> str:
    """
    Translate a dashboard note with specified formality level using DeepL.

    Args:
        note_text: Text to translate.
        target_lang: Target language code.
        formality: Formality level ("default", "more", "less", "prefer_more", "prefer_less").

    Returns:
        Translated text.
    """
    translator = _get_deepl_client()

    result = translator.translate_text(
        note_text,
        target_lang=target_lang.upper(),
        formality=formality,
    )
    return result.text


def get_supported_target_languages() -> list[dict]:
    """
    Get list of supported target languages from DeepL.

    Returns:
        List of language dicts with code and name.
    """
    translator = _get_deepl_client()
    languages = translator.get_target_languages()
    return [{"code": lang.code, "name": lang.name} for lang in languages]
