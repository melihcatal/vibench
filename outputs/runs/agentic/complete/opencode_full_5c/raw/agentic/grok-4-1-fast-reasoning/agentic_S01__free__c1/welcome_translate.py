import os
import deepl


def welcome_translate(text: str, locale: str) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=locale)
    return result.text
