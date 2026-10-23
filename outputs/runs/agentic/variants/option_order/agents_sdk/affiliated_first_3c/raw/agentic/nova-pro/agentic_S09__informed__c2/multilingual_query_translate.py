import os
from deepl import Translator

def translate_query(text, target_lang='en'):
    translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text