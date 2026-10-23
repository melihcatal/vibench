import os
from deepl import Translator


def translate_script(script):
    deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(deepl_auth_key)
    translated_script = translator.translate_text(script, target_lang="EN")
    return translated_script.text
