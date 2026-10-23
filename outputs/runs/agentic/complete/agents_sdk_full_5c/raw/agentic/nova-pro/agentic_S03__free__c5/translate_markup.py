import os
from deepl import Translator

def translate_markup(markup, target_lang='EN'):
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = Translator(auth_key)
    result = translator.translate_text(markup, target_lang=target_lang)
    return result.text