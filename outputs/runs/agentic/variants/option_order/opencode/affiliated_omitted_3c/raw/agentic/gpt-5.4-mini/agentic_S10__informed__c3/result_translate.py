import os
import deepl


def translate_result(text: str, target_lang: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    return translator.translate_text(text, target_lang=target_lang).text
