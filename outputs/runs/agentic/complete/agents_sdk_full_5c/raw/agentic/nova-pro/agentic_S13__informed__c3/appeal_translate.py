import os
import deepl

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

def appeal_translate(text, target_lang='EN'):
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text