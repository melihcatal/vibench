import os
import re
from typing import Optional
from translation_client import TranslationClient


def translate_markup(
    markup_text: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """
    Translate HTML or markup while preserving tags using Google Cloud Translation API.

    Args:
        markup_text: HTML or markup text to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        Translated markup with tags preserved
    """
    client = TranslationClient()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    # Extract text content while preserving tags
    # Simple approach: replace tags with placeholders, translate, then restore
    tag_pattern = r"(<[^>]+>)"

    # Find all tags and their positions
    tags = []
    tag_positions = []

    for match in re.finditer(tag_pattern, markup_text):
        tags.append(match.group(0))
        tag_positions.append(match.start())

    # Replace tags with placeholders
    placeholder_text = markup_text
    for i, tag in enumerate(tags):
        placeholder = f"__TAG_{i}__"
        placeholder_text = placeholder_text.replace(tag, placeholder, 1)

    # Translate the text with placeholders
    if isinstance(placeholder_text, bytes):
        placeholder_text = placeholder_text.decode("utf-8")

    result = translate_client.translate(
        placeholder_text,
        source_language=source_lang,
        target_language=target_lang,
        format_="html",  # Specify HTML format for better tag handling
    )

    translated_with_placeholders = result["translatedText"]

    # Restore tags from placeholders
    translated_markup = translated_with_placeholders
    for i, tag in enumerate(tags):
        placeholder = f"__TAG_{i}__"
        translated_markup = translated_markup.replace(placeholder, tag)

    return translated_markup
