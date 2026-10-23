"""Translate a single text string using DeepL."""

from __future__ import annotations

from typing import Any, Dict, Optional

import deepl

from translation_client import get_deepl_client, get_source_language, get_target_language
from translation_models import TextTranslationRequest, TextTranslationResponse, normalize_single_translation


def translate_text(text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> str:
    request = TextTranslationRequest(text=text, source_lang=source_lang, target_lang=target_lang)
    client = get_deepl_client()
    source = get_source_language(request.source_lang)
    target = get_target_language(request.target_lang)
    result = client.translate_text(request.text, source_lang=source, target_lang=target)
    return normalize_single_translation(result.text)


def translate_text_response(text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> TextTranslationResponse:
    translated_text = translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return TextTranslationResponse(text=text, translated_text=translated_text, source_lang=source_lang, target_lang=target_lang)


__all__ = ["translate_text", "translate_text_response", "deepl"]
