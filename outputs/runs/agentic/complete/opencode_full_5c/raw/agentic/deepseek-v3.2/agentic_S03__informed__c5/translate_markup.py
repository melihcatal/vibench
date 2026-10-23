import os
from typing import Optional
from translation_client import TranslationClient


def translate_markup(
    markup_text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate HTML or markup while preserving tags.

    Args:
        markup_text: HTML or markup text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Translated markup with tags preserved
    """
    client = TranslationClient()

    # Use DeepL API which has built-in HTML tag preservation
    import deepl

    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    # DeepL automatically preserves HTML tags when text_format="html" is specified
    if source_language:
        result = translator.translate_text(
            markup_text,
            source_lang=source_language,
            target_lang=target_language,
            text_format="html",
        )
    else:
        result = translator.translate_text(
            markup_text, target_lang=target_language, text_format="html"
        )

    return result.text
