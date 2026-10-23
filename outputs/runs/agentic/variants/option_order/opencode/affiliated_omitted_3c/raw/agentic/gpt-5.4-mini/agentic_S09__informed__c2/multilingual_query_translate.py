import os

from deepl import Translator


def multilingual_query_translate(query: str, target_lang: str) -> str:
    translator = Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
