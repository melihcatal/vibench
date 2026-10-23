import os
from deepl import Translator
from typing import Optional

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))

def translate_payload(text: str, target_language: Optional[str] = "ES") -> str:
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
