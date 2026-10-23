import os

from deepl import Translator


def translate_query(query: str, target_lang: str = "EN-US"):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = Translator(auth_key)
    return translator.translate_text(query, target_lang=target_lang).text
