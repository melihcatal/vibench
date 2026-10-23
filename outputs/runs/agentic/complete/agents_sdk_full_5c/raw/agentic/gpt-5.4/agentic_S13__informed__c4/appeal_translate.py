from __future__ import annotations

import os

import deepl


def appeal_translate(text: str, target_lang: str, source_lang: str | None = None) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality="default",
    )
    return {
        "provider": "DeepL API",
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
        "translated_text": result.text,
    }
