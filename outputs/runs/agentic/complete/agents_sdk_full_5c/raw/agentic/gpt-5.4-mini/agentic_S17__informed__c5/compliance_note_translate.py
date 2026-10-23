from __future__ import annotations

from typing import Any, Dict

import deepl


def translate_compliance_note(text: str, target_lang: str = "DE") -> Dict[str, Any]:
    translator = deepl.Translator(__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "translated_text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", None),
    }
