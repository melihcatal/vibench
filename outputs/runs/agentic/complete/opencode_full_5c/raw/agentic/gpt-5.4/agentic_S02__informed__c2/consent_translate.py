from __future__ import annotations

import os

import deepl


def consent_translate(
    text: str, target_lang: str, source_lang: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        preserve_formatting=True,
    )
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "text": result.text,
    }
