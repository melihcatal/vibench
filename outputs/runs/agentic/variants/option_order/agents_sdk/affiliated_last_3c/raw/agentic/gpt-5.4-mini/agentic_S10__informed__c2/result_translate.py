import os

import deepl

TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "EN-US")


def translate_result(text: str, target_language: str = TARGET_LANGUAGE) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    client = deepl.Translator(auth_key)
    result = client.translate_text(text, target_lang=target_language)
    return str(result)
