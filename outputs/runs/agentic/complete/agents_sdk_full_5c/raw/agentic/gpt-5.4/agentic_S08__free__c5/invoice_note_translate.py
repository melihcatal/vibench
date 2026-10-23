from __future__ import annotations

from typing import Any, Dict

import deepl



def translate_invoice_note(text: str, target_lang: str = "EN-US") -> Dict[str, Any]:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "billed_characters": getattr(result, "billed_characters", None),
    }
