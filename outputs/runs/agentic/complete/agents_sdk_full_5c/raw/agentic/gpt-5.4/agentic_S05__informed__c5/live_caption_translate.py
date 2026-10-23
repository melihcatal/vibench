from __future__ import annotations

import os

import deepl

from speech_models import normalize_text


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def translate_live_caption(text: str, *, target_language: str, source_language: str | None = None) -> str:
    auth_key = os.getenv(DEEPL_AUTH_KEY_ENV)
    if not auth_key:
        raise RuntimeError(f"Missing required environment variable: {DEEPL_AUTH_KEY_ENV}")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        normalize_text(text),
        source_lang=source_language,
        target_lang=target_language,
        model_type="prefer_quality_optimized",
    )
    return result.text
