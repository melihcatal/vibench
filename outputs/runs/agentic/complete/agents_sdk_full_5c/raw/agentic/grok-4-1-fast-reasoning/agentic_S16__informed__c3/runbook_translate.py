import deepl
import os

def translate_runbook_notes(notes: str, target_lang: str = 'en') -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(notes, target_lang=target_lang)
    return result.text
