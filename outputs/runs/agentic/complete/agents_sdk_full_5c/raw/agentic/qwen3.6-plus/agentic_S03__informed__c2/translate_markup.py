"""Translate HTML or markup while preserving tags using DeepL API."""

import os
import re
from deepl import Translator

from translation_models import TranslationRequest, TranslationResponse


def translate_markup(
    markup_text: str,
    target_lang: str,
    source_lang: str | None = None,
    tag_pattern: str = r"<[^>]+>",
) -> TranslationResponse:
    """Translate HTML/markup text while preserving tags using DeepL.

    DeepL supports an optional tag_handling='html' mode which tells the
    translator to treat input as HTML and ignore tags. This function wraps
    that capability and falls back to manual tag extraction if needed.

    Args:
        markup_text: HTML or markup text to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'JA').
        source_lang: Source language code. If None, DeepL auto-detects.
        tag_pattern: Regex pattern to identify tags (default matches HTML tags).

    Returns:
        TranslationResponse with translated markup and metadata.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access")

    translator = Translator(auth_key)

    kwargs: dict[str, str | None] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    try:
        result = translator.translate_text(
            markup_text,
            tag_handling="html",
            ignore_tags=["script", "style"],
            **kwargs,
        )
    except Exception:
        tags = re.findall(tag_pattern, markup_text)
        placeholder_map: dict[str, str] = {}
        working_text = markup_text
        for idx, tag in enumerate(tags):
            placeholder = f"__TAG_PLACEHOLDER_{idx}__"
            placeholder_map[placeholder] = tag
            working_text = working_text.replace(tag, placeholder, 1)

        result = translator.translate_text(working_text, **kwargs)

        translated = result.text
        for placeholder, tag in placeholder_map.items():
            translated = translated.replace(placeholder, tag)

        return TranslationResponse(
            translated_text=translated,
            source_lang=getattr(result, "detected_source_lang", None) or source_lang or "auto",
            target_lang=target_lang,
            provider="deepl",
            model_id="deepl-free" if "api-free.deepl.com" in str(getattr(translator, "server_url", "")) else "deepl-pro",
        )

    return TranslationResponse(
        translated_text=result.text,
        source_lang=getattr(result, "detected_source_lang", None) or source_lang or "auto",
        target_lang=target_lang,
        provider="deepl",
        model_id="deepl-free" if "api-free.deepl.com" in str(getattr(translator, "server_url", "")) else "deepl-pro",
    )
