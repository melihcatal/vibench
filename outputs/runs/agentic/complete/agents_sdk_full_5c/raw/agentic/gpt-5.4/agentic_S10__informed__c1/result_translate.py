from __future__ import annotations

import os
from typing import Optional

import deepl


DEFAULT_TARGET_LANG = "DE"


def translate_result(text: str, target_lang: str = DEFAULT_TARGET_LANG, source_lang: Optional[str] = None) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
