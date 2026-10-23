from deepl import Translator
import os

def translate_compliance_note(note: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text