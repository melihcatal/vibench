import os
from deepl import Translator


def translate_appeal(text, target_lang="EN"):
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
