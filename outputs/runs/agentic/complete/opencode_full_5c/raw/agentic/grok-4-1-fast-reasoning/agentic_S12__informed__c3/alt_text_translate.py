import os
import deepl

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def alt_text_translate(alt_text: str, target_language: str = "ES") -> str:
    result = translator.translate_text(alt_text, target_lang=target_language)
    return result.text
