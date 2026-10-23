from __future__ import annotations

import os
from typing import Optional

import deepl

from security_models import TranslationResult


DEEPL_DEFAULT_TARGET = "EN-US"


def translate_runbook_notes(text: str, target_language: str = DEEPL_DEFAULT_TARGET, source_language: Optional[str] = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        preserve_formatting=True,
    )
    detected_source = source_language or getattr(result, "detected_source_lang", None)
    return TranslationResult(
        source_language=detected_source,
        target_language=target_language,
        translated_text=result.text,
    )
