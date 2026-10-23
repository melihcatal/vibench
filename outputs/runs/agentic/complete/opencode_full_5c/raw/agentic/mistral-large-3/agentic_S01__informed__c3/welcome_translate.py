import os
from typing import Dict, Any
from deepl import Translator


def welcome_translate(text: str, target_lang: str) -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
