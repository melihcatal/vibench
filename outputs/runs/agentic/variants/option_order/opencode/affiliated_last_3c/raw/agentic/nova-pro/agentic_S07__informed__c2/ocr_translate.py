import os
import deepl


def translate_text(text):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang="EN-US")
    return result.text
