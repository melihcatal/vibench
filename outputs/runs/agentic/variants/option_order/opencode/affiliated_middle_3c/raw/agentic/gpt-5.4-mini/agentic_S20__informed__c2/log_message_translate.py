import os

from deepl import Translator


def log_message_translate(text: str, target_lang: str = "FR") -> dict:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translation": str(result), "target_lang": target_lang}
