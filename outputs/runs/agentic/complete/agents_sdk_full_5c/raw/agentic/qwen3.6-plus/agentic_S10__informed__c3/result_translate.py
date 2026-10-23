"""
Translate generated model output using the DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import os
from typing import List, Optional

import deepl

from model_models import TranslationResult


DEEPL_MODEL_NAME = "deepl-free"  # or "deepl-pro" for paid tier


def load_deepl_auth_key() -> str:
    """Load the DeepL authentication key from environment."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required. "
            "Sign up at https://www.deepl.com/pro-api to get your key."
        )
    return auth_key


def create_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create a configured DeepL translator client."""
    key = auth_key or load_deepl_auth_key()
    return deepl.Translator(key)


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> TranslationResult:
    """Translate text using the DeepL API.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g., 'EN', 'DE', 'FR', 'JA').
        source_language: Source language code, or None for auto-detection.
        auth_key: Optional override for the DeepL auth key.

    Returns:
        TranslationResult with translated text and metadata.
    """
    translator = create_deepl_translator(auth_key)

    source_lang = source_language.upper() if source_language else None
    target_lang = target_language.upper()

    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    detected_source = source_lang if source_lang else "auto"
    # DeepL returns the detected source language in result.detected_source_lang
    if hasattr(result, "detected_source_lang") and result.detected_source_lang:
        detected_source = result.detected_source_lang

    return TranslationResult(
        translated_text=result.text,
        source_language=detected_source.lower(),
        target_language=target_lang.lower(),
        raw_response=result,
    )


def translate_batch(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[TranslationResult]:
    """Translate a batch of texts using the DeepL API.

    Args:
        texts: List of texts to translate.
        target_language: Target language code.
        source_language: Source language code, or None for auto-detection.
        auth_key: Optional override for the DeepL auth key.

    Returns:
        List of TranslationResult objects.
    """
    translator = create_deepl_translator(auth_key)

    source_lang = source_language.upper() if source_language else None
    target_lang = target_language.upper()

    # DeepL supports batch translation with translate_text for list inputs
    results = translator.translate_text(
        texts,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    out: List[TranslationResult] = []
    for result in results:
        detected_source = source_lang if source_lang else "auto"
        if hasattr(result, "detected_source_lang") and result.detected_source_lang:
            detected_source = result.detected_source_lang
        out.append(
            TranslationResult(
                translated_text=result.text,
                source_language=detected_source.lower(),
                target_language=target_lang.lower(),
                raw_response=result,
            )
        )

    return out


def translate_model_output(
    generated_text: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> TranslationResult:
    """Convenience: translate model-generated output to a target language."""
    return translate_text(
        text=generated_text,
        target_language=target_language,
        source_language=source_language,
    )
