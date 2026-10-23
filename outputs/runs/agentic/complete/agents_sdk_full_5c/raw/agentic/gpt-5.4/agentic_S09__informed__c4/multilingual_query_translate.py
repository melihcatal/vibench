from __future__ import annotations

import os

import deepl


DEEPL_MODEL_TYPE = "quality_optimized"


def translate_query(
    query: str,
    *,
    target_lang: str,
    source_lang: str | None = None,
    preserve_formatting: bool = True,
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required for DeepL translation")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        query,
        target_lang=target_lang,
        source_lang=source_lang,
        preserve_formatting=preserve_formatting,
        model_type=DEEPL_MODEL_TYPE,
    )
    return result.text
