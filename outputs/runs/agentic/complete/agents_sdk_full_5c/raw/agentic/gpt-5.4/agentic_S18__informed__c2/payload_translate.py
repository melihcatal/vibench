from __future__ import annotations

import os
from typing import Optional

import deepl

from messaging_models import TranslationResult


DEEPL_DEFAULT_TARGET = os.environ.get("DEEPL_TARGET_LANG", "EN")


def translate_payload_text(text: str, *, target_language: str = DEEPL_DEFAULT_TARGET, source_language: Optional[str] = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    detected = source_language or getattr(result, "detected_source_lang", None)
    return TranslationResult(
        translated_text=result.text,
        source_language=detected,
        target_language=target_language,
        provider="DeepL API",
    )
