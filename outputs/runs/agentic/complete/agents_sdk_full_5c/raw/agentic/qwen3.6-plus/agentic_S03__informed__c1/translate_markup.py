"""
Translates HTML or markup while preserving tags.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import re
from typing import List, Optional

from translation_client import get_client
from translation_models import TranslationResult


def translate_markup(
    markup_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    ignore_tags: Optional[List[str]] = None,
) -> TranslationResult:
    """
    Translate HTML or XML markup text while preserving all tags.

    Uses DeepL's tag_handling parameter to ensure tags like <div>, <span>,
    <p>, <a>, etc. are preserved and not translated.

    Args:
        markup_text: HTML or XML markup text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code (optional).
        formality: Formality level ('prefer_more' or 'prefer_less'; optional).
        ignore_tags: Specific tag names to ignore entirely during translation.

    Returns:
        TranslationResult with translated markup, tags preserved.
    """
    client = get_client()
    tag_handling = "html"
    if not _looks_like_html(markup_text):
        tag_handling = "xml"

    result = client.translate(
        text=markup_text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
        tag_handling=tag_handling,
        ignore_tags=ignore_tags,
    )
    return result


def translate_html_content(
    html_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    """
    Specifically translate HTML content, preserving all HTML tags and attributes.

    Args:
        html_text: Full HTML string to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional).
        formality: Formality level (optional).

    Returns:
        TranslationResult with translated HTML content.
    """
    return translate_markup(
        markup_text=html_text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
        ignore_tags=["script", "style", "code", "pre"],
    )


def translate_inline_markup(
    text_with_inline_tags: str,
    target_lang: str,
    source_lang: Optional[str] = None,
) -> str:
    """
    Translate text containing inline tags (like <b>, <i>, <em>, <strong>).

    Args:
        text_with_inline_tags: Text with inline markup.
        target_lang: Target language code.
        source_lang: Source language code (optional).

    Returns:
        Translated text with inline tags preserved.
    """
    result = translate_markup(
        markup_text=text_with_inline_tags,
        target_lang=target_lang,
        source_lang=source_lang,
        ignore_tags=["b", "i", "em", "strong", "span"],
    )
    return result.text


def _looks_like_html(text: str) -> bool:
    """Check if the text contains common HTML elements."""
    html_tags = re.compile(
        r"<(html|head|body|div|span|p|h[1-6]|a|ul|ol|li|table|tr|td|th|"
        r"form|input|button|select|option|img|br|hr|nav|header|footer|"
        r"section|article|aside|main)\b",
        re.IGNORECASE,
    )
    return bool(html_tags.search(text))


if __name__ == "__main__":
    html = "<p>Hello <b>world</b>, welcome to our <span>site</span>!</p>"
    result = translate_markup(html, target_lang="DE")
    print(result.text)
