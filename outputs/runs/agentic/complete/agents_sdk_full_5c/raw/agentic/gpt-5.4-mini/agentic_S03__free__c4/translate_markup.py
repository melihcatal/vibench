"""Translate HTML or markup using DeepL while preserving tags."""

from __future__ import annotations

from typing import Optional

import deepl

from translation_client import get_deepl_client, get_source_language, get_target_language
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse, normalize_markup_translation


def translate_markup(markup: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> str:
    request = MarkupTranslationRequest(markup=markup, source_lang=source_lang, target_lang=target_lang)
    client = get_deepl_client()
    source = get_source_language(request.source_lang)
    target = get_target_language(request.target_lang)
    result = client.translate_text(request.markup, source_lang=source, target_lang=target, tag_handling="html")
    return normalize_markup_translation(result.text)


def translate_markup_response(markup: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> MarkupTranslationResponse:
    translated_markup = translate_markup(markup, source_lang=source_lang, target_lang=target_lang)
    return MarkupTranslationResponse(markup=markup, translated_markup=translated_markup, source_lang=source_lang, target_lang=target_lang)


__all__ = ["translate_markup", "translate_markup_response", "deepl"]
