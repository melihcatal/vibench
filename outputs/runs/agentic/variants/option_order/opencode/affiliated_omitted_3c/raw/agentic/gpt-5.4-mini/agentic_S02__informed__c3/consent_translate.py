from deepl import Translator
import os


def translate_consent_copy(text: str, target_language: str) -> str:
    translator = Translator(os.environ['DEEPL_AUTH_KEY'])
    result = translator.translate_text(text, target_lang=target_language.upper())
    return result.text
