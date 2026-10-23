import os

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

from deepl import Translator


def dashboard_note_translate(text, target_lang="en"):
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
