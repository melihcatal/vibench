import os
from typing import Dict

from deepl import Translator


def translate_log_message(text: str, target_lang: str = "DE") -> Dict[str, str]:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": str(result), "target_lang": target_lang}
