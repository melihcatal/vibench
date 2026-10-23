from __future__ import annotations

import os

import deepl


def translate_ocr_text(text: str, target_lang: str, source_lang: str | None = None) -> dict:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "DeepL API",
        "detected_source_lang": getattr(result, "detected_source_lang", None),
        "target_lang": target_lang,
        "text": result.text,
        "model_type_used": getattr(result, "model_type_used", None),
    }
