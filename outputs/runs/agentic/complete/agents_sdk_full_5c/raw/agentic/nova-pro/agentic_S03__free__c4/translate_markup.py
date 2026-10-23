import os
from deepl import Translator

deepl_auth_key = os.getenv('DEEPL_AUTH_KEY')

translator = Translator(deepl_auth_key)

def translate_markup(markup, target_lang='EN'):
    result = translator.translate_text(markup, target_lang=target_lang)
    return result.text