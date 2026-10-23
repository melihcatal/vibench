import deepl
import os
from typing import Optional

translator = deepl.Translator(os.getenv('DEEPL_AUTH_KEY'))

def translate_log_message(message: str, target_lang: str = 'FR') -> str:
    result = translator.translate_text(message, target_lang=target_lang)
    return result.text
