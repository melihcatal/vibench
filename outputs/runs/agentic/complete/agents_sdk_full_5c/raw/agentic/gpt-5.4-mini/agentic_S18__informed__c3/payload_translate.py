from __future__ import annotations

from typing import Dict

from deepl import Translator


def translate_payload_text(text: str, target_lang: str = "EN-US") -> Dict[str, str]:
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": str(result), "target_lang": target_lang}
