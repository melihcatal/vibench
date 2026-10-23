from __future__ import annotations

import deepl

from speech_models import TranslationResult


PROVIDER = "deepl"
MODEL_TYPE = "prefer_quality_optimized"


def translate_script(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = deepl.Translator()
    response = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        model_type=MODEL_TYPE,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", None),
        provider=PROVIDER,
    )
