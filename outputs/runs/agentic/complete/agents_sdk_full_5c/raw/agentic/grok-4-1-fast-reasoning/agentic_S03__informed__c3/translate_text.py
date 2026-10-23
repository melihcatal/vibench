import os
from typing import Optional
from deepl import Translator

def translate_text(text: str, source_lang: Optional[str] = None, target_lang: str) -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text