from __future__ import annotations

import os
from typing import Dict

import deepl


DEEPL_TARGET_LANG_ENV = "DEEPL_TARGET_LANG"


def translate_payload_text(text: str, target_lang: str | None = None, source_lang: str | None = None) -> Dict[str, str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    target = target_lang or os.getenv(DEEPL_TARGET_LANG_ENV, "EN-US")
    result = translator.translate_text(text, target_lang=target, source_lang=source_lang)
    return {
        "provider": "deepl",
        "target_lang": result.target_lang,
        "detected_source_lang": result.detected_source_lang,
        "text": result.text,
    }
