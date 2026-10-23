import os
from deepl import Translator

deepl_auth_key = os.environ['DEEPL_AUTH_KEY']

def translate_text(text, target_lang='EN'):
    translator = Translator(deepl_auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text