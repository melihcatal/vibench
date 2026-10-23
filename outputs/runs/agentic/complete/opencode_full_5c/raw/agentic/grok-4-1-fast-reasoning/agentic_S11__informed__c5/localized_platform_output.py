import os
import deepl


def localize_platform_output(text: str, target_lang: str = "FR") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return text
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
