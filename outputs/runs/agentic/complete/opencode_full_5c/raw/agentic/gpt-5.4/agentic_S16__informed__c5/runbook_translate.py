from __future__ import annotations

import deepl

from security_client import get_deepl_api_key
from security_models import TranslationResult


def runbook_translate(text: str, target_language: str) -> TranslationResult:
    translator = deepl.Translator(get_deepl_api_key())
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        source_language=result.detected_source_lang,
        target_language=target_language,
        translated_text=result.text,
        provider="deepl",
    )
