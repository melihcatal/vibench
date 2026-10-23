import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def appeal_translate(text):
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang="EN")
    return result.text
