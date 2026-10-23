import os
from deepl import Translator


def appeal_translate(appeal_text: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return appeal_text  # fallback

    translator = Translator(auth_key)
    result = translator.translate_text(appeal_text, target_lang=target_lang)
    return result.text
