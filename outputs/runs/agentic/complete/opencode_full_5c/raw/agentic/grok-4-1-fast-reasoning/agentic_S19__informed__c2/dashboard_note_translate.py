import os
import deepl


def dashboard_note_translate(note: str, target_locale: str = "FR") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_locale)
    return result.text
