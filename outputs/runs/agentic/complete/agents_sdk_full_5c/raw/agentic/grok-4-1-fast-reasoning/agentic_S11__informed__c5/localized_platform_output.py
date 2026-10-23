import os
import deepl
from typing import Optional

def localized_platform_output(text: str, target_language: str = 'FR') -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError('DEEPL_AUTH_KEY not set')
    translator = deepl.Translator(auth_key)
    translated = translator.translate_text(text, target_lang=target_language)
    return translated.text
