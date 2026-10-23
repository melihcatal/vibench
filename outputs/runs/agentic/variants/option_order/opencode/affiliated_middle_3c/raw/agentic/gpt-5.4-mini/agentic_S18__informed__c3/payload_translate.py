from deepl import Translator
import os


def translate_payload_text(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
