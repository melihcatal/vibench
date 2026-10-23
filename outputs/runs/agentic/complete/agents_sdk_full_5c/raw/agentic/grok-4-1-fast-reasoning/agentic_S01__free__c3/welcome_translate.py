import os
from deepl import Translator

def welcome_translate(text: str, target_locale: str) -> str:
    api_key = os.getenv('DEEPL_AUTH_KEY')
    if not api_key:
        raise ValueError('DEEPL_AUTH_KEY not set')
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return result.text