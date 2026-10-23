import os
import deepl


def translate_alt_text(text: str, target_lang: str = "en") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
