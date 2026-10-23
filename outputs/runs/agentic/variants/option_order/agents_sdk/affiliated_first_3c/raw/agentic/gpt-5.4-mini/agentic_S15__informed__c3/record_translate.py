"""Translate user-facing document fields using DeepL API."""
from __future__ import annotations

from typing import Any, Dict, Iterable

import deepl


def record_translate(text: str, target_lang: str = "EN-US") -> Dict[str, Any]:
    translator = deepl.Translator(auth_key=os.getenv("DEEPL_AUTH_KEY", ""))
    translated = translator.translate_text(text, target_lang=target_lang)
    return {"provider": "deepl", "target_lang": target_lang, "text": translated.text}
