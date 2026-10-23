import deepl
import os

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_consent_copy(text: str, target_lang: str = "EN-US") -> str:
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
