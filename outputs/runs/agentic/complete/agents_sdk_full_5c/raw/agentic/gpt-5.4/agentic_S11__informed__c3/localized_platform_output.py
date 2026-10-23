from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


DEFAULT_TARGET_LANG = "DE"


def localize_platform_output(text: str, target_lang: str = DEFAULT_TARGET_LANG) -> TranslationResult:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return TranslationResult(
        text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        raw=result,
    )
