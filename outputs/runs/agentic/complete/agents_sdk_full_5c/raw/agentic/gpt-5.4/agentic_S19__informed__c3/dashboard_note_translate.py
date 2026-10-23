from __future__ import annotations

import os
from typing import Optional

import deepl

from observability_models import TranslationResult


def dashboard_note_translate(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        preserve_formatting=True,
    )
    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        target_language=target_language.upper(),
        detected_source_language=getattr(result, "detected_source_lang", source_language),
    )
