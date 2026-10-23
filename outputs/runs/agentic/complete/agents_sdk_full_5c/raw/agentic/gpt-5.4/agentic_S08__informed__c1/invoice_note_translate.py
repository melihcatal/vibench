from __future__ import annotations

import os
from typing import Any, Dict

import deepl



def invoice_note_translate(text: str, target_lang: str = "EN") -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "translated_text": result.text,
    }
