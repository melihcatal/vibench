from deepl import Translator
import os

def dashboard_note_translate(note: str, target_lang: str = "FR") -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    translator = Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text