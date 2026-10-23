from __future__ import annotations

import os
from typing import Any, Dict

import deepl


def dashboard_note_translate(
    text: str, target_lang: str, source_lang: str | None = None
) -> Dict[str, Any]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "DeepL",
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
    }
