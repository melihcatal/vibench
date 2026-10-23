from __future__ import annotations

import os

import deepl

from document_models import normalize_text


def translate_ocr_text(text: str, target_lang: str, source_lang: str | None = None, model_type: str = "quality_optimized") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        normalize_text(text),
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=model_type,
    )
    return result.text
