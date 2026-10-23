from __future__ import annotations

from typing import Optional

from deep_translator import DeeplTranslator


def translate_alt_text(text: str, target_language: str = "es", source_language: Optional[str] = None) -> str:
    translator = DeeplTranslator(api_key=None)
    if source_language:
        translator.source = source_language
    translator.target = target_language
    return translator.translate(text)
