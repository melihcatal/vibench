import os

from deepl import Translator


def alt_text_translate(text: str, target_lang: str):
    translator = Translator(auth_key=os.environ.get("DEEPL_AUTH_KEY", ""))
    return translator.translate_text(text, target_lang=target_lang).text
