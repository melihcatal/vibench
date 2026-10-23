from __future__ import annotations

from typing import Dict

from deepl import Translator


def invoice_note_translate(text: str, target_language: str = "EN-US") -> Dict[str, str]:
    translator = Translator(auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_language)
    return {"translated_text": result.text, "detected_source_language": getattr(result, "detected_source_lang", "")}
