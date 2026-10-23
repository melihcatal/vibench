"""
Translate a single text string between languages.

Provider: DeepL Translation API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

import deepl

from translation_client import create_translation_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_source_language,
    parse_deepl_response,
)


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> TranslationResponse:
    """
    Translate a single text string from source to target language using DeepL.

    Args:
        text: The text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'JA', 'ZH').
            DeepL also supports regional variants like 'EN-US', 'EN-GB',
            'PT-BR', 'PT-PT'.
        source_lang: Source language code, or None for auto-detection.
            When None, DeepL automatically detects the source language.
            Supported codes include 'EN', 'DE', 'FR', 'ES', 'IT', 'PT',
            'NL', 'PL', 'RU', 'JA', 'ZH', 'KO', 'AR', 'BG', 'CS', 'DA',
            'EL', 'ET', 'FI', 'HU', 'ID', 'LT', 'LV', 'NB', 'RO', 'SK',
            'SL', 'SV', 'TR', 'UK'.
        formality: Controls formality level for supported languages.
            Values: 'more', 'less', 'prefer_more', 'prefer_less', 'default'.
        preserve_formatting: Whether to preserve formatting in the translation.
        client: Optional pre-created DeepL Translator client.

    Returns:
        TranslationResponse with the translated text and metadata.

    Raises:
        deepl.DeepLException: If the DeepL API request fails.
        ValueError: If the request is invalid.
    """
    req = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
        preserve_formatting=preserve_formatting,
    )

    errors = req.validate()
    if errors:
        raise ValueError(f"Invalid translation request: {'; '.join(errors)}")

    normalized_source = normalize_source_language(source_lang)
    normalized_target = target_lang.strip().upper()

    if client is None:
        client = create_translation_client()

    translate_kwargs = {
        "target_lang": normalized_target,
        "preserve_formatting": preserve_formatting,
    }

    if normalized_source is not None:
        translate_kwargs["source_lang"] = normalized_source

    if formality is not None:
        translate_kwargs["formality"] = formality

    result = client.translate_text(text, **translate_kwargs)

    return parse_deepl_response(result)


if __name__ == "__main__":
    response = translate_text(
        text="Hello, how are you today?",
        target_lang="DE",
    )
    if response.is_success:
        print(f"Translated: {response.first_text}")
