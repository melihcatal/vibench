import os
import deepl
from typing import Optional

def translate_runbook_notes(text: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text