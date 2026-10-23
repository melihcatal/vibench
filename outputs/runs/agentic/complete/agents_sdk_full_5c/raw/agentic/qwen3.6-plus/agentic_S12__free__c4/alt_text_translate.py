"""
Translate generated image descriptions using DeepL API.
Provider: DeepL API (deepl)
Endpoint: api.deepl.com
Model: DeepL Translation v2
"""

from __future__ import annotations

import os
from typing import Optional

import deepl


def translate_alt_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> dict:
    """
    Translate generated image alt text or descriptions using DeepL API.

    Args:
        text: The alt text or description to translate.
        target_language: BCP-47 target language code (e.g., 'DE', 'FR', 'JA').
        source_language: Optional source language code. Auto-detected if None.
        formality: Optional formality level ('more', 'less', 'default').

    Returns:
        Dictionary with translated text, source language, and target language.

    Raises:
        ValueError: If DEEPL_AUTH_KEY environment variable is not set.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language

    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, target_lang=target_language, **translate_kwargs)

    return {
        "provider": "deepl",
        "original_text": text,
        "translated_text": result.text,
        "source_language": result.detected_source_lang,
        "target_language": target_language,
    }


def translate_alt_text_batch(
    texts: list[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> list[dict]:
    """
    Translate multiple alt texts in a batch using DeepL API.

    Args:
        texts: List of alt texts or descriptions to translate.
        target_language: BCP-47 target language code.
        source_language: Optional source language code.

    Returns:
        List of translation result dictionaries.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language

    results = translator.translate_text(texts, target_lang=target_language, **translate_kwargs)

    output = []
    for original, translated in zip(texts, results):
        output.append({
            "provider": "deepl",
            "original_text": original,
            "translated_text": translated.text,
            "source_language": translated.detected_source_lang,
            "target_language": target_language,
        })

    return output


def translate_description_for_locales(
    description: str,
    locales: list[str],
    formality: Optional[str] = None,
) -> dict[str, str]:
    """
    Translate an image description for multiple locales.

    Args:
        description: The image description to translate.
        locales: List of target locale codes (e.g., ['DE', 'FR', 'JA', 'ZH']).
        formality: Optional formality level.

    Returns:
        Dictionary mapping locale code to translated text.
    """
    translations = {}
    for locale in locales:
        try:
            result = translate_alt_text(
                text=description,
                target_language=locale,
                formality=formality,
            )
            translations[locale] = result["translated_text"]
        except Exception:
            translations[locale] = description
    return translations


def get_supported_languages() -> list[dict]:
    """
    Get list of supported languages from DeepL API.

    Returns:
        List of language dictionaries with code, name, and support info.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)
    source_languages = translator.get_source_languages()
    target_languages = translator.get_target_languages()

    return {
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_languages
        ],
        "target_languages": [
            {
                "code": lang.code,
                "name": lang.name,
                "supports_formality": getattr(lang, "supports_formality", False),
            }
            for lang in target_languages
        ],
    }


if __name__ == "__main__":
    import sys
    import json

    text = sys.argv[1] if len(sys.argv) > 1 else "A scenic mountain landscape"
    target = sys.argv[2] if len(sys.argv) > 2 else "DE"

    result = translate_alt_text(text=text, target_language=target)
    print(json.dumps(result, indent=2))
