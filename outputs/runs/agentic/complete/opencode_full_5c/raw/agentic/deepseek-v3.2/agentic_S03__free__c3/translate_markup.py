import os
import re
from typing import Optional
from google.cloud import translate_v2 as translate


def translate_markup(
    markup_text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate HTML or markup text while preserving tags using Google Cloud Translation API.

    Args:
        markup_text: HTML or markup text containing tags
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Translated markup text with tags preserved
    """
    client = translate.Client()

    if source_language:
        result = client.translate(
            markup_text,
            target_language=target_language,
            source_language=source_language,
            format_="html",
        )
    else:
        result = client.translate(
            markup_text, target_language=target_language, format_="html"
        )

    return result["translatedText"]
