import deepl
import os
from typing import Optional

def translate_compliance_note(note: str, target_lang: str = "EN-US") -> str:
    """
    Translates encryption or compliance notes using DeepL API.
    """
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
