from deepl import Translator
import os

def translate_secret_runbook_notes(runbook_text: str, target_lang: str = 'EN-US') -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = Translator(auth_key)
    result = translator.translate_text(runbook_text, target_lang=target_lang)
    return result.text
