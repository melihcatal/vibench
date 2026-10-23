import deepl
import os
from typing import Optional

def alt_text_translate(text: str, target_lang: str = "ES") -> str:
    translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)