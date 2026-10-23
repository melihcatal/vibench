import os
from deepl import Translator


def translate_text(text):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang="EN")
    return result.text
