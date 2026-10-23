from __future__ import annotations

import os
from typing import Dict, Optional

import deepl


def translate_invoice_note(text: str, target_lang: str = "EN-US", source_lang: Optional[str] = None) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "deepl",
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
    }
