import os
from deepl import Translator


def multilingual_query_translate(query: str, target_lang: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    translator = Translator(auth_key)
    response = translator.translate_text(query, target_lang=target_lang)
    return response.text
