import deepl
import os
from typing import List


def translate_log_messages(messages: List[str], target_lang: str = "ES") -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated = []
    for msg in messages:
        result = translator.translate_text(msg, target_lang=target_lang)
        translated.append(result.text)
    return translated
