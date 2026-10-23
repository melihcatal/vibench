import os
import deepl
from typing import Optional


def ocr_translate(
    text: str, source_lang: Optional[str] = None, target_lang: str = "ES"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
