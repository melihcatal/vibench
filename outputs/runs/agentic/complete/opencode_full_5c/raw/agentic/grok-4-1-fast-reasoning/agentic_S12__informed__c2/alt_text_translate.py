import os
import deepl


def alt_text_translate(alt_text: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(alt_text, target_lang=target_lang)
    return result.text
