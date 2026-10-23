import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def welcome_translate(text: str, target_lang: str = "en") -> str:
    """
    Translates onboarding copy into the user's locale using DeepL.
    """
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
