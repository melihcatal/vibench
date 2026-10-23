from __future__ import annotations

import deepl

from document_models import normalize_text


DEFAULT_TARGET_LANG = "EN-US"


def translate_ocr_text(text: str, target_lang: str = DEFAULT_TARGET_LANG, source_lang: str | None = None) -> str:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(normalize_text(text), target_lang=target_lang, source_lang=source_lang)
    return result.text
