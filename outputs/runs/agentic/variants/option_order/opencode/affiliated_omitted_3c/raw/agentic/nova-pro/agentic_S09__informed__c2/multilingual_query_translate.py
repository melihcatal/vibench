import os
from deepl import Translator


def translate_query(query: str, target_lang: str) -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
