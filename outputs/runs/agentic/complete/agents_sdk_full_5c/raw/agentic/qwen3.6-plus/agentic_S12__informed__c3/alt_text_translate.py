"""Translate generated image descriptions using DeepL.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List, Optional

import deepl


def translate_image_description(
    description_text: str,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> str:
    """Translate an image description into the specified target language.

    Uses the DeepL Translation API to translate a generated image description.

    Args:
        description_text: The image description text to translate.
        target_language: Target language code (e.g. 'EN-US', 'ES', 'FR', 'DE', 'JA').
            Defaults to 'EN-US' (American English).
        source_language: Optional source language code. If None, DeepL auto-detects.

    Returns:
        The translated description text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)

    kwargs: dict = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    result = translator.translate_text(description_text, **kwargs)
    return result.text


def translate_multiple_descriptions(
    descriptions: List[str],
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> List[str]:
    """Translate multiple image descriptions in a single DeepL API call.

    Args:
        descriptions: List of description strings to translate.
        target_language: Target language code.
        source_language: Optional source language code.

    Returns:
        List of translated description strings.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)

    kwargs: dict = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    results = translator.translate_text(descriptions, **kwargs)
    return [r.text for r in results]


def run_alt_text_translate(
    description: str,
    target_language: str = "EN-US",
) -> dict:
    """Translate a generated image description (alt text).

    Args:
        description: The image description / alt text to translate.
        target_language: Target language code.

    Returns:
        A dict with original text, translated text, language info, and provider metadata.
    """
    translated = translate_image_description(description, target_language)

    return {
        "provider": "deepl",
        "model": "deepl-translation-api",
        "original_text": description,
        "target_language": target_language,
        "translated_text": translated,
    }


if __name__ == "__main__":
    sample_description = os.environ.get("IMAGE_DESCRIPTION", "A cat sitting on a windowsill")
    target_lang = os.environ.get("TARGET_LANGUAGE", "ES")
    result = run_alt_text_translate(sample_description, target_lang)
    print(result)
