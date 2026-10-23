from __future__ import annotations

import os
from typing import Dict

import deepl


PROVIDER = "deepl"


def translate_payload_text(text: str, target_lang: str, source_lang: str | None = None) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": PROVIDER,
        "text": result.text,
        "detected_source_language": getattr(result, "detected_source_lang", source_lang or ""),
        "target_language": target_lang,
    }
