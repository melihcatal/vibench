from deepl import Translator
import os

def translate_runbook_notes(text: str, source_lang: str = "ES", target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text