import os

from deepl import Translator


def log_message_translate(text: str, target_lang: str = "DE") -> str:
    translator = Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
