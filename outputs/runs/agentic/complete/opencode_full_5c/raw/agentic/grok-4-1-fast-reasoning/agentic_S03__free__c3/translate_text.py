import deepl
import os
from typing import Optional

def translate_text(text: str, source_lang: Optional[str] = "auto", target_lang: str) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text
