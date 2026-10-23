import os
import deepl
from typing import Optional


def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
