"""
Translate narration scripts before synthesis using DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Optional, List, Dict, Any

import deepl

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"

# DeepL supported source/target language codes
DEEPL_LANGUAGES = {
    "en": "EN",
    "es": "ES",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "pt": "PT",
    "nl": "NL",
    "ja": "JA",
    "zh": "ZH",
    "ko": "KO",
    "ru": "RU",
    "ar": "AR",
    "bg": "BG",
    "cs": "CS",
    "da": "DA",
    "el": "EL",
    "et": "ET",
    "fi": "FI",
    "hu": "HU",
    "id": "ID",
    "lt": "LT",
    "lv": "LV",
    "no": "NB",
    "pl": "PL",
    "ro": "RO",
    "sk": "SK",
    "sl": "SL",
    "sv": "SV",
    "tr": "TR",
    "uk": "UK",
}


def get_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create a DeepL translator client.

    Args:
        auth_key: DeepL auth key. Falls back to DEEPL_AUTH_KEY env var.

    Returns:
        Initialized deepl.Translator instance.
    """
    key = auth_key or os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not key:
        raise ValueError(
            f"DeepL auth key not provided. Set {DEEPL_AUTH_KEY_ENV}."
        )
    return deepl.Translator(key)


def translate_script(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """Translate a narration script using DeepL.

    Args:
        text: Source text to translate.
        target_lang: Target language code (e.g. 'ES', 'FR', 'JA').
        source_lang: Source language code (auto-detected if None).
        auth_key: DeepL auth key.
        formality: Formality level ('more', 'less', 'prefer_more', 'prefer_less', 'default').

    Returns:
        Translated text string.
    """
    translator = get_deepl_translator(auth_key)

    target_upper = target_lang.upper()
    source_upper = source_lang.upper() if source_lang else None

    kwargs: Dict[str, Any] = {
        "source_lang": source_upper,
        "target_lang": target_upper,
    }

    if formality:
        kwargs["formality"] = formality

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_script_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[str]:
    """Batch translate multiple narration scripts using DeepL.

    Args:
        texts: List of source texts.
        target_lang: Target language code.
        source_lang: Source language code (auto-detected if None).
        auth_key: DeepL auth key.
        formality: Formality level.

    Returns:
        List of translated texts.
    """
    translator = get_deepl_translator(auth_key)

    target_upper = target_lang.upper()
    source_upper = source_lang.upper() if source_lang else None

    kwargs: Dict[str, Any] = {
        "source_lang": source_upper,
        "target_lang": target_upper,
    }

    if formality:
        kwargs["formality"] = formality

    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]


def detect_and_translate(
    text: str,
    target_lang: str,
    auth_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Detect source language and translate narration script.

    Args:
        text: Source text.
        target_lang: Target language code.
        auth_key: DeepL auth key.

    Returns:
        Dict with detected language, translation, and metadata.
    """
    translator = get_deepl_translator(auth_key)

    # DeepL auto-detects source when source_lang is not specified
    result = translator.translate_text(
        text,
        target_lang=target_lang.upper(),
    )

    return {
        "original_text": text,
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
    }
