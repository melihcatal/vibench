from __future__ import annotations

import os
from typing import Any, Dict, Optional

import deepl



def invoice_note_translate(text: str, target_lang: str, source_lang: Optional[str] = None) -> Dict[str, Any]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "DeepL",
        "detected_source_language": getattr(result, "detected_source_lang", source_lang),
        "target_language": target_lang,
        "translated_text": result.text,
    }
