from __future__ import annotations

import os

import deepl


def translate_consent_copy(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        preserve_formatting=True,
    )
    return result.text
