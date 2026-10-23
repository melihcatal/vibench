import deepl
import os
from typing import str

def translate_log_message(text: str, target_lang: str = 'ES') -> str:
    """
    Translate support-visible log messages for another locale using DeepL API.
    """
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
