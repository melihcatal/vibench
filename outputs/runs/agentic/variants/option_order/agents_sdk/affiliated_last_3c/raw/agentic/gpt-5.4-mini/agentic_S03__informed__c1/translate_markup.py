from __future__ import annotations

from translation_client import translate_markup_text


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    return translate_markup_text(markup, source_language, target_language)
