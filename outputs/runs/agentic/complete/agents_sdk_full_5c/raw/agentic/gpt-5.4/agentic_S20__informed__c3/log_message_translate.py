from __future__ import annotations

import os

import deepl


DEEPL_MODEL_TYPE = os.getenv("DEEPL_MODEL_TYPE", "prefer_quality_optimized")


def translate_log_message(text: str, target_lang: str, source_lang: str | None = None) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return result.text
