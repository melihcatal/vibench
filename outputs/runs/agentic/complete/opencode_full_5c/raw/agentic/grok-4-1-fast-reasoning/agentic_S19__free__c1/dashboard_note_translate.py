import os
import deepl
from typing import Optional


def translate_dashboard_note(
    note: str, target_lang: str = "FR", source_lang: str = "EN"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        note, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
