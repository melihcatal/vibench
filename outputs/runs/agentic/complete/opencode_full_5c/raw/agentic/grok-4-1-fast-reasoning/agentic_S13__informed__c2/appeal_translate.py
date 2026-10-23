import deepl
import os
from typing import Optional

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def appeal_translate(text: str, target_lang: str = "EN-US") -> str:
    """
    Translate appeal text for review using DeepL API.
    """
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
