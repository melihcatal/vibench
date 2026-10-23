from __future__ import annotations

import os

import deepl


def translate_record_text(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return result.text
