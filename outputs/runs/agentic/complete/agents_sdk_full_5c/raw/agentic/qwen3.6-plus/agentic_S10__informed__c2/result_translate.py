"""
Translate generated model output text.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
Endpoint: api.deepl.com/v2/translate
"""

import os
from typing import List, Optional

import deepl


def _resolve_deepl_config() -> str:
    """Resolve DeepL API key from environment variables."""
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY is required for DeepL translation integration"
        )
    return api_key


def create_deepl_translator() -> deepl.Translator:
    """Create and return a configured DeepL Translator instance."""
    api_key = _resolve_deepl_config()
    return deepl.Translator(api_key)


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate text using the DeepL API.

    Provider: DeepL Translation API
    Endpoint: api.deepl.com/v2/translate

    Args:
        text: The text to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'DE', 'JA').
        source_lang: Optional source language code. DeepL will auto-detect
                     if not provided.
        formality: Optional formality level ('more' or 'less') for languages
                   that support it.

    Returns:
        The translated text string.
    """
    translator = create_deepl_translator()

    translate_kwargs: dict = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, **translate_kwargs)
    return result.text


def translate_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
) -> List[str]:
    """
    Translate a list of texts using the DeepL API.

    Provider: DeepL Translation API

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'DE').
        source_lang: Optional source language code.

    Returns:
        List of translated text strings in the same order as input.
    """
    translator = create_deepl_translator()

    translate_kwargs: dict = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    results = translator.translate_text(texts, **translate_kwargs)
    return [result.text for result in results]


def translate_model_output(
    model_output: str,
    target_languages: List[str],
    source_lang: Optional[str] = None,
) -> dict:
    """
    Translate LLM model output into multiple target languages via DeepL.

    Args:
        model_output: The text output from a hosted LLM.
        target_languages: List of target language codes.
        source_lang: Optional source language code.

    Returns:
        Dictionary mapping language codes to their translations.
    """
    translations = {}
    for lang in target_languages:
        translations[lang.upper()] = translate_text(
            text=model_output,
            target_lang=lang,
            source_lang=source_lang,
        )
    return translations
