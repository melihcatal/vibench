import os
import deepl


def alt_text_translate(description: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(description, target_lang=target_lang)
    return result.text
