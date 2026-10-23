import os
from deepl import Translator


def translate_query(query, target_lang="EN-US"):
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
