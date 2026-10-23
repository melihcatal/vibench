from __future__ import annotations

from typing import Dict

from deepl import Translator


def invoice_note_translate(text: str, target_lang: str = "EN-US") -> Dict[str, object]:
    translator = Translator(auth_key="${DEEPL_AUTH_KEY}")
    result = translator.translate_text(text, target_lang=target_lang)
    return {"source_text": text, "translated_text": result.text, "detected_source_language": getattr(result, "detected_source_lang", None)}
