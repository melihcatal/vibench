from __future__ import annotations

from typing import Optional

import deepl


def translate_invoice_note(
    text: str, target_lang: str = "EN-US", source_lang: Optional[str] = None
) -> str:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
