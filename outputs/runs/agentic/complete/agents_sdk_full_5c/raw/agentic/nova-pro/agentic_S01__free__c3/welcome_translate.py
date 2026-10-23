import os
from deepl import Translator

DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

def translate_welcome(text, target_lang):
    translator = Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text