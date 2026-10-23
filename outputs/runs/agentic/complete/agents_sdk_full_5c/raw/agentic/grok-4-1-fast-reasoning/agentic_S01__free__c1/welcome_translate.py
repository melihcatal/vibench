import os
from deepl import Translator

def translate_onboarding_copy(text: str, target_locale: str) -> str:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return result.text