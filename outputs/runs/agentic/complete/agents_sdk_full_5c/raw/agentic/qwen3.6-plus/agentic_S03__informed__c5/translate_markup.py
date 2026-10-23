"""
translate_markup.py - Translates HTML or markup while preserving tags using DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY environment variable
"""

from typing import Optional

from translation_models import (
    extract_text_from_markup,
    rebuild_markup,
)
from translation_client import TranslationClient


def translate_markup(
    markup: str,
    target_lang: str = "en",
    source_lang: Optional[str] = None,
) -> str:
    """
    Translate HTML or markup content from source_lang to target_lang using the DeepL API,
    preserving all HTML tags, attributes, and structure.

    DeepL's built-in HTML tag_handling is used to ensure tags are not translated
    and the output structure matches the input.

    Args:
        markup: The HTML/markup string to translate.
        target_lang: Target language code (e.g., 'en', 'de', 'fr'). Defaults to 'en'.
        source_lang: Source language code. If None, DeepL auto-detects the source.

    Returns:
        The translated HTML/markup string with tags preserved.

    Raises:
        ValueError: If markup is empty.
        deepl.DeepLException: If the DeepL API request fails.
    """
    if not markup or not markup.strip():
        raise ValueError("Input markup must not be empty.")

    # Use DeepL's native HTML translation support with tag_handling="html"
    # This preserves tags automatically without manual extraction/rebuilding
    client = TranslationClient()

    result = client.translate_html_segments(
        segments=[markup.strip()],
        source_lang=source_lang,
        target_lang=target_lang,
    )

    if not result:
        return markup

    return result[0]
