import os

from deepl import Translator


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    translator = Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    return translator.translate_text(query, target_lang=target_language).text
