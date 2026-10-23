import os
import deepl


def welcome_translate(text: str, target_locale: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return result.text
