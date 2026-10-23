"""
translate_text.py - Translates a single text string between languages using DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY environment variable
"""

from typing import Optional

from translation_models import TranslationRequest, TranslationResponse
from translation_client import TranslationClient


def translate_text(
    text: str,
    target_lang: str = "en",
    source_lang: Optional[str] = None,
    formal: bool = False,
) -> TranslationResponse:
    """
    Translate a single text string from source_lang to target_lang using the DeepL API.

    Args:
        text: The text string to translate.
        target_lang: Target language code (e.g., 'en', 'de', 'fr'). Defaults to 'en'.
        source_lang: Source language code. If None, DeepL auto-detects the source.
        formal: Whether to prefer formal language (supported for some target languages).

    Returns:
        TranslationResponse with translated text and metadata.

    Raises:
        ValueError: If text is empty or target_lang is invalid.
        deepl.DeepLException: If the DeepL API request fails.
    """
    if not text or not text.strip():
        raise ValueError("Input text must not be empty.")

    request = TranslationRequest(
        text=text.strip(),
        source_lang=source_lang,
        target_lang=target_lang,
        formal=formal,
    )

    client = TranslationClient()

    response = client.translate(
        text=request.text,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        preserve_formatting=request.preserve_formatting,
        formal=request.formal,
    )

    return response
