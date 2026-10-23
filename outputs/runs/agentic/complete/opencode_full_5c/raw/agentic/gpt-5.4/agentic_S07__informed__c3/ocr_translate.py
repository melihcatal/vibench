from __future__ import annotations

import os

import deepl


def translate_ocr_text(
    text: str, target_lang: str, source_lang: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", source_lang),
        "target_lang": target_lang,
        "provider": "deepl",
    }
