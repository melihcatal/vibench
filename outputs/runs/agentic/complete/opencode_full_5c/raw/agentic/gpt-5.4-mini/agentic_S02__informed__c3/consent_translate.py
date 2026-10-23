import os

from deepl import Translator


def consent_translate(text: str, target_lang: str) -> str:
    translator = Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    return translator.translate_text(text, target_lang=target_lang).text
