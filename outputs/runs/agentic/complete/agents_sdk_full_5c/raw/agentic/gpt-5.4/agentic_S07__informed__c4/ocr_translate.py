from __future__ import annotations

import os

import deepl

from document_models import normalize_text


def translate_ocr_text(text: str, target_language: str, source_language: str | None = None) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        normalize_text(text),
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        preserve_formatting=True,
    )
    return {
        "provider": "deepl",
        "text": result.text,
        "detected_source_language": getattr(result, "detected_source_lang", None),
        "target_language": target_language.upper(),
    }
