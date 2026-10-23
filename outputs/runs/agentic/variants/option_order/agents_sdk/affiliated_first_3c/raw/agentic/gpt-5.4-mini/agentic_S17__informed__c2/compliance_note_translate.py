from __future__ import annotations

import os
from typing import Any, Dict

from deepl import Translator

DEEPL_TARGET_LANG = "EN-US"


def translate_compliance_note(text: str, target_lang: str = DEEPL_TARGET_LANG, auth_key: str | None = None) -> Dict[str, Any]:
    translator = Translator(auth_key or os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "service": "DeepL API",
        "target_lang": target_lang,
        "translated_text": result.text,
    }
