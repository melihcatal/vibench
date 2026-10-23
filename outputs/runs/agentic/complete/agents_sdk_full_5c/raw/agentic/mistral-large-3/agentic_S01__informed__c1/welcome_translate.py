import os
from typing import Dict
import deepl


def translate_welcome_message(text: str, target_lang: str) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    
    result = translator.translate_text(
        text,
        target_lang=target_lang
    )
    
    return result.text