import os
from deepl import Translator


def translate_text(text):
    translator = Translator(api_key=os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang="EN")
    return result.text
