import os
import deepl
from typing import Optional


def translate_appeal(
    text: str, target_lang: str = "EN", source_lang: Optional[str] = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
