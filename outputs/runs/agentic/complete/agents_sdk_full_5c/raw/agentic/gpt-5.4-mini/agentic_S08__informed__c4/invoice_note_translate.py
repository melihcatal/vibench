from __future__ import annotations

from typing import Any, Dict

from deepl import Translator


def invoice_note_translate(text: str, target_lang: str = "EN-US") -> Dict[str, Any]:
    translator = Translator(__import__('os').environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text, "detected_source_language": getattr(result, "detected_source_lang", None)}
