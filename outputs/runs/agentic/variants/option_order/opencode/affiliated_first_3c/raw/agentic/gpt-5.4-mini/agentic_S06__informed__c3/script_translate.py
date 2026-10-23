import os

from deepl import Translator

from speech_models import normalize_text


def translate_script(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    return normalize_text(translator.translate_text(text, target_lang=target_lang).text)
