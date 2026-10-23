import os
from typing import Dict, Any
import deepl

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_invoice_note(text: str, target_lang: str = "EN-US") -> str:
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text