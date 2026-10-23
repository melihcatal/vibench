import os
import deepl


def translate_query(query, target_lang="EN-US"):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text

