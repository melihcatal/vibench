import os
from deepl import Translator

def alt_text_translate(text: str, target_lang: str = 'ES') -> str:
    translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text