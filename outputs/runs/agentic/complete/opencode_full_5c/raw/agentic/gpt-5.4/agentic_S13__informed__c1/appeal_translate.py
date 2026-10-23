from __future__ import annotations

import os

import deepl


def appeal_translate(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    translator = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        formality="default",
    )
    return str(result.text)
