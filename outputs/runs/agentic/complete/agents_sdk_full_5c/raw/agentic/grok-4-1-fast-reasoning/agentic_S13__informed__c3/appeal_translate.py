import os
from deepl import Translator
from typing import Optional

def translate_appeal(appeal_text: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    translator = Translator(auth_key)
    result = translator.translate_text(appeal_text, target_lang=target_lang)
    return result.text
