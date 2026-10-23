from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


def welcome_translate(
    text: str, target_locale: str, source_locale: str | None = None
) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_locale.upper(),
        source_lang=source_locale.upper() if source_locale else None,
    )
    return TranslationResult(
        translated_text=result.text,
        source_language=getattr(result, "detected_source_lang", source_locale),
        target_language=target_locale,
        provider="deepl",
    )
