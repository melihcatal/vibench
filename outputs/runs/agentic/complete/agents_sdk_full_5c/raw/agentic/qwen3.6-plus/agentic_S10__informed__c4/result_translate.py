"""
Translate generated model output using DeepL API.
Provider: DeepL (deepl SDK, DEEPL_AUTH_KEY)
"""

import os
from typing import Optional, List

import deepl


def _get_deepl_translator() -> deepl.Translator:
    """Create and return an authenticated DeepL translator."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(auth_key)


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate text using DeepL Translation API.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'ES', 'FR', 'DE', 'JA').
        source_language: Source language code (auto-detected if None).
        formality: 'more' or 'less' for languages that support formality.

    Returns:
        Translated text string.
    """
    translator = _get_deepl_translator()

    kwargs: dict = {}
    if source_language:
        kwargs["source_lang"] = source_language
    if formality:
        kwargs["formality"] = formality

    result = translator.translate_text(text, target_lang=target_language, **kwargs)
    return result.text


def translate_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple texts using DeepL API in one request.

    Args:
        texts: List of texts to translate.
        target_language: Target language code.
        source_language: Source language code.

    Returns:
        List of translated texts.
    """
    translator = _get_deepl_translator()

    kwargs: dict = {}
    if source_language:
        kwargs["source_lang"] = source_language

    results = translator.translate_text(
        texts, target_lang=target_language, **kwargs
    )

    if isinstance(results, list):
        return [r.text for r in results]
    return [results.text]


def translate_model_output(
    output_text: str,
    target_languages: List[str],
    source_language: Optional[str] = None,
) -> dict:
    """
    Translate a model output into multiple target languages.

    Args:
        output_text: The model-generated text to translate.
        target_languages: List of target language codes.
        source_language: Source language code.

    Returns:
        Dict mapping language codes to translated text.
    """
    translations = {}
    for lang in target_languages:
        try:
            translations[lang] = translate_text(
                output_text, lang, source_language=source_language
            )
        except Exception as e:
            translations[lang] = f"Translation error: {str(e)}"
    return translations
