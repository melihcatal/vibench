import os
from deepl import Translator
from typing import Optional
from document_client import validate_env

validate_env("deepl")


def invoice_note_translate(note: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
