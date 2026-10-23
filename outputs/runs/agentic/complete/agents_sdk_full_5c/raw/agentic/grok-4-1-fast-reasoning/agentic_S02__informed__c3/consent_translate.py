import os
import deepl
from typing import Optional

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

def translate_consent(text: str, source_lang: Optional[str] = None, target_lang: str = "EN") -> str:
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text