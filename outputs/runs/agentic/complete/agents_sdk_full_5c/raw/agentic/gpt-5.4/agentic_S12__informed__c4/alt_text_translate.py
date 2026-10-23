from __future__ import annotations

import os

import deepl


PROVIDER = "DeepL API"


def translate_alt_text(text: str, target_lang: str, source_lang: str | None = None) -> dict:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": PROVIDER,
        "model": "deepl-translation",
        "target_lang": target_lang,
        "text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", source_lang),
    }
