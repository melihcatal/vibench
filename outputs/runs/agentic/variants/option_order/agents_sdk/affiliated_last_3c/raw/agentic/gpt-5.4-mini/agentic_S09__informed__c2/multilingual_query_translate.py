import os
from typing import List

from deepl import Translator


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    translator = Translator(auth_key)
    result = translator.translate_text(query, target_lang=target_language.upper())
    return result.text


def multilingual_query_translate_batch(queries: List[str], target_language: str = "en") -> List[str]:
    return [multilingual_query_translate(q, target_language=target_language) for q in queries]
