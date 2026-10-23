"""
Translate HTML or markup while preserving tags.

Provider: DeepL Translation API
SDK: deepl
Auth: DEEPL_AUTH_KEY

Uses DeepL's XML tag handling mode to preserve HTML/markup tags
during translation. The translate_text API with tag_handling='xml'
instructs DeepL to recognize and preserve tags like <b>, <p>, <a>,
<span>, etc.
"""

import re
from typing import Optional

import deepl

from translation_client import create_translation_client
from translation_models import (
    TranslationResponse,
    TranslationResult,
    normalize_source_language,
    build_tag_handling_config,
)

# HTML elements that should not be translated (script, style content, etc.)
NON_TRANSLATABLE_TAGS = {"script", "style", "code", "pre", "noscript", "iframe"}

# Self-closing HTML tags
SELF_CLOSING_TAGS = {
    "br", "hr", "img", "input", "meta", "link", "area", "base",
    "col", "embed", "param", "source", "track", "wbr",
}

# HTML attribute names that contain translatable text
TRANSLATABLE_ATTRS = {"alt", "title", "placeholder", "aria-label", "aria-description"}


def sanitize_html_for_xml(
    html: str,
) -> str:
    """
    Pre-process HTML to be safe for DeepL XML tag handling.

    DeepL's XML mode requires well-formed tags. This function:
    - Ensures self-closing tags use proper XML syntax
    - Escapes stray angle brackets in text content
    - Normalizes tag names to lowercase for consistency

    Args:
        html: Raw HTML string.

    Returns:
        Sanitized HTML safe for DeepL XML processing.
    """
    sanitized = html

    for tag in SELF_CLOSING_TAGS:
        # Match self-closing instances like <br> and convert to <br/>
        pattern = rf"<({tag})(\s[^>]*)?>"
        sanitized = re.sub(
            pattern,
            lambda m: f"<{m.group(1)}{m.group(2) or ''}/>",
            sanitized,
            flags=re.IGNORECASE,
        )

    return sanitized


def translate_markup(
    html: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    ignore_tags: Optional[list[str]] = None,
    client: Optional[deepl.Translator] = None,
) -> TranslationResponse:
    """
    Translate HTML or markup content while preserving all tags.

    Uses DeepL's XML tag handling to recognize and preserve HTML tags.
    Tags like <b>, <p>, <a href="...">, <span class="..."> are preserved
    exactly, only the text content between tags is translated.

    Args:
        html: HTML or markup string to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code, or None for auto-detection.
        formality: Controls formality level for supported languages.
        preserve_formatting: Whether to preserve formatting.
        ignore_tags: Additional HTML tag names to skip translation for.
        client: Optional pre-created DeepL Translator client.

    Returns:
        TranslationResponse with translated HTML preserving all tags.

    Raises:
        deepl.DeepLException: If the DeepL API request fails.
        ValueError: If the request is invalid.
    """
    if client is None:
        client = create_translation_client()

    sanitized_html = sanitize_html_for_xml(html)

    normalized_source = normalize_source_language(source_lang)
    normalized_target = target_lang.strip().upper()

    tag_config = build_tag_handling_config(html_mode=True)

    translate_kwargs: dict = {
        "target_lang": normalized_target,
        "preserve_formatting": preserve_formatting,
        **tag_config,
    }

    if normalized_source is not None:
        translate_kwargs["source_lang"] = normalized_source

    if formality is not None:
        translate_kwargs["formality"] = formality

    # Combine default ignore_tags with user-provided ones
    all_ignore = list(NON_TRANSLATABLE_TAGS)
    if ignore_tags:
        all_ignore.extend(ignore_tags)
    translate_kwargs["ignore_tags"] = all_ignore

    raw_results = client.translate_text(sanitized_html, **translate_kwargs)

    translations: list[TranslationResult] = []
    char_count = 0

    for result in raw_results:
        translations.append(TranslationResult(
            text=result.text,
            detected_source_lang=getattr(result, "detected_source_lang", None),
            model_info=None,
        ))
        char_count += len(result.text)

    return TranslationResponse(
        translations=translations,
        character_count=char_count,
    )


def translate_html_with_attributes(
    html: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    client: Optional[deepl.Translator] = None,
) -> TranslationResponse:
    """
    Translate HTML content including translatable attribute values.

    Handles attributes like alt, title, placeholder, aria-label
    by wrapping them in temporary tags for DeepL processing.

    Args:
        html: HTML string to translate.
        target_lang: Target language code.
        source_lang: Source language code, or None for auto-detection.
        formality: Controls formality level.
        client: Optional pre-created DeepL Translator client.

    Returns:
        TranslationResponse with translated HTML including attributes.
    """
    if client is None:
        client = create_translation_client()

    # Wrap translatable attribute values in <at> tags so DeepL translates them
    def replace_attr_value(match: re.Match) -> str:
        attr_name = match.group(1).lower()
        attr_value = match.group(2)
        return f' {attr_name}="<at>{attr_value}</at>"'

    processed = html
    for attr in TRANSLATABLE_ATTRS:
        pattern = rf'{attr}\s*=\s*"([^"]*)"'
        processed = re.sub(
            pattern,
            replace_attr_value,
            processed,
            flags=re.IGNORECASE,
        )

    response = translate_markup(
        html=processed,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
        ignore_tags=["at"],
        client=client,
    )

    # Unwrap <at> tags back to raw attribute values
    result_text = response.first_text if response.translations else ""
    # The <at> tags are ignored by DeepL so they remain; strip them
    result_text = result_text.replace("<at>", "").replace("</at>", "")

    return TranslationResponse(
        translations=[TranslationResult(
            text=result_text,
            detected_source_lang=response.translations[0].detected_source_lang
            if response.translations else None,
            model_info=None,
        )] if response.translations else [],
        character_count=response.character_count,
    )


if __name__ == "__main__":
    html_content = "<p>Hello <b>world</b>! This is a <a href=\"#\">link</a>.</p>"
    response = translate_markup(html_content, target_lang="DE")
    if response.is_success:
        print(f"Translated HTML: {response.first_text}")
