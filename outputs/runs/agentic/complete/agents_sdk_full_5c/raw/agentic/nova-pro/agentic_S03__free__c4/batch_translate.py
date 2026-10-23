import os
from deepl import Translator

deepl_auth_key = os.getenv('DEEPL_AUTH_KEY')

translator = Translator(deepl_auth_key)

def batch_translate(texts, target_lang='EN'):
    results = translator.translate_text(texts, target_lang=target_lang)
    return [result.text for result in results]