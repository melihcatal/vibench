import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

def appeal_translate(text, target_lang='en'):
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text