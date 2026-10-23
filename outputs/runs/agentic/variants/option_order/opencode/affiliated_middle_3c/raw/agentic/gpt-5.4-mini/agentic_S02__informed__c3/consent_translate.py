import os
from deepl import Translator


def translate_consent_copy(text, target_lang='EN-US'):
    translator = Translator(os.environ.get('DEEPL_AUTH_KEY', ''))
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
