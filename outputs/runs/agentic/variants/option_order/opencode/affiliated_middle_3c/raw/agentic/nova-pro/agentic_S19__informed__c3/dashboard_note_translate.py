import os

import deepl


def dashboard_note_translate(text, target_lang):
    api_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
