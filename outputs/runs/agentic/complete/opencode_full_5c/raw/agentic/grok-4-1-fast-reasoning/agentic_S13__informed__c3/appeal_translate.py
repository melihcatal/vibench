import os
import deepl
from typing import Optional

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def appeal_translate(appeal_text: str, target_lang: str = "EN-US") -> str:
    result = translator.translate_text(appeal_text, target_lang=target_lang)
    return result.text
