import os
from deepl import Translator, TargetLanguage


def translate_result(text: str, target_lang: str = "FR") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=TargetLanguage(target_lang))
    return result.text
