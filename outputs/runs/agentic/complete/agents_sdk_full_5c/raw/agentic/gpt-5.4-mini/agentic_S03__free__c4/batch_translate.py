"""Batch translate strings using DeepL while preserving order."""

from __future__ import annotations

from typing import Iterable, List, Optional

import deepl

from translation_client import get_deepl_client, get_source_language, get_target_language
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_batch_translations


def batch_translate(texts: Iterable[str], source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> List[str]:
    request = BatchTranslationRequest(texts=list(texts), source_lang=source_lang, target_lang=target_lang)
    client = get_deepl_client()
    source = get_source_language(request.source_lang)
    target = get_target_language(request.target_lang)
    result = client.translate_text(request.texts, source_lang=source, target_lang=target)
    return normalize_batch_translations(result)


def batch_translate_response(texts: Iterable[str], source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> BatchTranslationResponse:
    translated_texts = batch_translate(texts, source_lang=source_lang, target_lang=target_lang)
    return BatchTranslationResponse(texts=list(texts), translated_texts=translated_texts, source_lang=source_lang, target_lang=target_lang)


__all__ = ["batch_translate", "batch_translate_response", "deepl"]
