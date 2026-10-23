"""
alt_text_translate.py - Translate generated image descriptions
using the DeepL Translation API.

Provider: DeepL
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
import sys
import json
from typing import Optional, List

import deepl


def translate_alt_text(
    text: str,
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> str:
    """
    Translate an image description (alt text) into a target language
    using the DeepL Translation API.

    Args:
        text: The image description text to translate.
        target_language: ISO language code for target language (e.g., "ES", "FR", "DE").
        source_language: ISO language code for source language (optional, auto-detected if None).

    Returns:
        Translated text string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable must be set "
            "for DeepL API access."
        )

    translator = deepl.Translator(auth_key)

    translate_kwargs = {
        "target_lang": target_language,
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language

    result = translator.translate_text(text, **translate_kwargs)
    return result.text


def translate_multiple_alt_texts(
    texts: List[str],
    target_language: str = "ES",
    source_language: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple image descriptions in a single DeepL API call.

    Args:
        texts: List of description strings to translate.
        target_language: Target language code.
        source_language: Source language code (optional).

    Returns:
        List of translated text strings.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable must be set "
            "for DeepL API access."
        )

    translator = deepl.Translator(auth_key)

    translate_kwargs = {
        "target_lang": target_language,
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language

    results = translator.translate_text(texts, **translate_kwargs)
    return [r.text for r in results]


def translate_pipeline_descriptions(
    pipeline_output: dict,
    target_languages: Optional[List[str]] = None,
) -> dict:
    """
    Translate image descriptions from pipeline output into multiple languages.

    Args:
        pipeline_output: Dict with a 'description' key containing the alt text.
        target_languages: List of target language codes. Defaults to ["ES", "FR", "DE"].

    Returns:
        Dict mapping language codes to translated descriptions.
    """
    if target_languages is None:
        target_languages = ["ES", "FR", "DE"]

    description = pipeline_output.get("description", "")
    if not description:
        return {}

    translations = {}
    for lang in target_languages:
        translated = translate_alt_text(description, target_language=lang)
        translations[lang] = translated

    return translations


def main():
    """CLI entry point for translating alt text."""
    if len(sys.argv) < 2:
        print("Usage: python alt_text_translate.py <description> [target_lang]")
        sys.exit(1)

    text = sys.argv[1]
    target_lang = sys.argv[2] if len(sys.argv) > 2 else "ES"

    try:
        translated = translate_alt_text(text, target_language=target_lang)
        print(f"Original ({target_lang} translation):")
        print(f"  {text}")
        print(f"  -> {translated}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
