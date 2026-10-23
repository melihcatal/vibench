import os

import deepl


def translate_consent_copy(text: str, target_language: str = "EN-US") -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
