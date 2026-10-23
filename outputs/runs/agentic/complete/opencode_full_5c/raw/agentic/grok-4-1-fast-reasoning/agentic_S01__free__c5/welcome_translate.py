import os
from deepl import Translator


def welcome_translate(onboarding_copy: str, locale: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(onboarding_copy, target_lang=locale)
    return str(result)
