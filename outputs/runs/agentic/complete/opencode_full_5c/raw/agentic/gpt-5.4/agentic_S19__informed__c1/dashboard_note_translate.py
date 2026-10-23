from __future__ import annotations

from typing import Any, Dict

import deepl


def dashboard_note_translate(
    text: str,
    target_lang: str,
    source_lang: str | None = None,
    formality: str | None = None,
) -> Dict[str, Any]:
    client = deepl.Translator(__import__("os").getenv("DEEPL_AUTH_KEY"))
    result = client.translate_text(
        text, target_lang=target_lang, source_lang=source_lang, formality=formality
    )
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "translated_text": result.text,
    }
