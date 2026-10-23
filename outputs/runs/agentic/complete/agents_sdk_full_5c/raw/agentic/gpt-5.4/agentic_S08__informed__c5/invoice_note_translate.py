from __future__ import annotations

import os
from typing import Any, Dict

import deepl


def invoice_note_translate(text: str, target_lang: str = "EN-US") -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "translated_text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", None),
    }
