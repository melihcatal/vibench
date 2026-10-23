import os
from deepl import Translator
from typing import Optional

def appeal_translate(text: str, target_lang: str = "EN") -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY not set")
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
