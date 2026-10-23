import os
from typing import Optional
import deepl

def translate_text(text: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text
