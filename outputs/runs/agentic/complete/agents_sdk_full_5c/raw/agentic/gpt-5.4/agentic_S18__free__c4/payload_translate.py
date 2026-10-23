from __future__ import annotations

from typing import Optional

import deepl


DEEPL_MODEL_PROVIDER = "api-free.deepl.com"


def translate_payload_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
    )
    return result.text
