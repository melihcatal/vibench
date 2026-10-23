import os
from deepl import Translator

def invoice_note_translate(text: str, target_lang: str = 'EN-US') -> str:
    auth_key = os.environ['DEEPL_AUTH_KEY']
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
