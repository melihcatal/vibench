import os
import deepl
from typing import Optional
from translation_client import get_deepl_auth_key

def translate_text(text: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    auth_key = get_deepl_auth_key()
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
