# [LATER-STEP] invoice_note_translate.py

# Translates extracted invoice notes using DeepL SDK

import os
from deepl import DeepL

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
assert DEEPL_AUTH_KEY, "Set DEEPL_AUTH_KEY"

translator = DeepL(DEEPL_AUTH_KEY)


def translate_note(text: str, target_lang: str = "EN") -> str:
    """Translate a free‑form note or description to the target language."""
    result = translator.translate_text(text, target_lang=target_lang)
    return result.translated_text
