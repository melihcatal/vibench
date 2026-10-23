import os
from deepl import Translator

translator = Translator(os.getenv('DEEPL_AUTH_KEY'))

def translate_alt_text(alt_text, target_lang='DE'):
    result = translator.translate_text(alt_text, target_lang=target_lang)
    return result.text