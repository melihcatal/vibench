from __future__ import annotations

import os

import deepl


def translate_invoice_note(
    text: str, target_lang: str = "EN-US", source_lang: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "DeepL API",
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
    }
