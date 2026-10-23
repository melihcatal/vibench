from __future__ import annotations

import os

import deepl


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(
        text,
        source_lang=source_language.upper() if source_language else None,
        target_lang=target_language.upper(),
        model_type="prefer_quality_optimized",
    )
    return result.text
