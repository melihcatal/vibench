import os
import deepl


def log_message_translate(message: str, target_lang: str = "es") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(message, target_lang=target_lang)
    return result.text
