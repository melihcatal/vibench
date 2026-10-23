import os
import deepl
from typing import Optional

def log_message_translate(text: str, target_lang: str = 'FR') -> str:
    \"\"\"Translate support-visible log messages for another locale using DeepL.\"\"\"
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
