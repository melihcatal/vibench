import os
import deepl


def translate_onboarding_copy(text: str, locale: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=locale)
    return result.text
