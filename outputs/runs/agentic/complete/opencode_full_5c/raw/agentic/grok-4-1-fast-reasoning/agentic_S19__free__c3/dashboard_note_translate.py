import os
import deepl
from typing import Optional


def translate_dashboard_note(
    note_text: str, target_language: str = "ES", source_language: Optional[str] = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        note_text, target_lang=target_language, source_lang=source_language
    )
    return result.text
