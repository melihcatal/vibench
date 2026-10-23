from __future__ import annotations

from typing import Optional

import deepl

DEEPL_MODEL = "DeepL API"


def invoice_note_translate(text: str, target_lang: str = "EN-US", auth_key: Optional[str] = None) -> str:
    translator = deepl.Translator(auth_key or "")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
