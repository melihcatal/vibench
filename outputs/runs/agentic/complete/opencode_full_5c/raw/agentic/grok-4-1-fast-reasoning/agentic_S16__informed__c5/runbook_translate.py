import deepl
import os


def translate_secret_runbook_runbook(notes: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(notes, target_lang=target_lang)
    return result.text
