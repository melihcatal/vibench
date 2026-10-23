from __future__ import annotations

import os

import deepl


DEEPL_MODEL_TYPE = "latency_optimized"


def translate_query(query: str, *, target_lang: str, source_lang: str | None = None) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL translation")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        query,
        source_lang=source_lang,
        target_lang=target_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return result.text
