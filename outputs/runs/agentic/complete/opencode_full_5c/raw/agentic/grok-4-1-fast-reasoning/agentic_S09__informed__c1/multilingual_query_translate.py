import os
import deepl
from typing import Optional


def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        query, target_lang=deepl.TargetLanguage(target_lang)
    )
    return result.text
