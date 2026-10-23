import os
from deepl import Translator

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_query(query, target_lang="en"):
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
