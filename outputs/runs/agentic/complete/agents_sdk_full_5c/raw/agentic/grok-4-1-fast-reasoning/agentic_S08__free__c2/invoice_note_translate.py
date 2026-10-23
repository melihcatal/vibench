import os
import deepl
from typing import Optional

def translate_invoice_note(note: str, target_lang: str = 'EN') -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
