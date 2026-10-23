from __future__ import annotations

import os

import deepl



def translate_appeal(text: str, target_lang: str = "EN-US", source_lang: str | None = None) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "detected_source_lang": getattr(result, "detected_source_lang", source_lang),
        "text": result.text,
    }
