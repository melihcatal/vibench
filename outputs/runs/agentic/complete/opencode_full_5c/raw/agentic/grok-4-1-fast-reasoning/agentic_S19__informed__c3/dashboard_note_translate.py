import deepl
import os


def dashboard_note_translate(note: str, target_lang: str = "FR") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
