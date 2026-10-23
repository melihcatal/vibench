"""Translate narration scripts before synthesis using DeepL API."""

import os
from typing import List, Optional

import deepl


def translate_script(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """Translate a narration script from one language to another using DeepL.

    DeepL provides high-quality translation for narration and voiceover scripts.
    Requires DEEPL_AUTH_KEY environment variable if auth_key is not provided.

    Args:
        text: The narration script text to translate.
        target_lang: Target language code (e.g. "EN-US", "DE", "JA", "ES").
        source_lang: Optional source language code (e.g. "EN", "FR"). DeepL auto-detects if None.
        auth_key: DeepL API key. Falls back to DEEPL_AUTH_KEY env var.
        formality: Optional formality level: "more", "less", "default", "prefer_more", "prefer_less".

    Returns:
        The translated script text.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DeepL API key required. Set DEEPL_AUTH_KEY or pass auth_key.")

    translator = deepl.Translator(key)

    translate_kwargs = {}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, target_lang=target_lang, **translate_kwargs)
    return result.text


def translate_scripts_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[str]:
    """Translate a batch of narration scripts using DeepL.

    Args:
        texts: List of narration script strings to translate.
        target_lang: Target language code.
        source_lang: Optional source language code for auto-detection override.
        auth_key: DeepL API key.

    Returns:
        List of translated script strings in the same order as input.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DeepL API key required. Set DEEPL_AUTH_KEY or pass auth_key.")

    translator = deepl.Translator(key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, **translate_kwargs)

    if isinstance(results, list):
        return [r.text for r in results]
    return [results.text]


def detect_script_language(
    text: str,
    auth_key: Optional[str] = None,
) -> Optional[str]:
    """Detect the language of a narration script using DeepL.

    Args:
        text: The script text to analyze.
        auth_key: DeepL API key.

    Returns:
        Detected language code (e.g. "EN", "DE", "JA") or None.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DeepL API key required. Set DEEPL_AUTH_KEY or pass auth_key.")

    translator = deepl.Translator(key)
    detections = translator.detect_language(text)

    if detections:
        return detections[0].code
    return None
