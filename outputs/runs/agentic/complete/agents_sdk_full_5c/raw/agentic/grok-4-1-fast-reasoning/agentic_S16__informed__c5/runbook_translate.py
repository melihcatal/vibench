import deepl
import os

def translate_runbook_notes(text: str, target_lang: str = "EN-US") -> str:
    translator = deepl.Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text