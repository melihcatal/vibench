import os
from deepl import Translator


def translate_markup(text, source_lang, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
