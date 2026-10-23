import os
import deepl
from typing import Optional


def translate_invoice_note(note: str, target_lang: str = "EN") -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
