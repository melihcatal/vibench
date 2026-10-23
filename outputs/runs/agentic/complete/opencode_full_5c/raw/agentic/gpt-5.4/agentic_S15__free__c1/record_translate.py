from __future__ import annotations

from typing import Any

import deepl


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def record_translate(
    document: dict[str, Any], fields: list[str], target_lang: str
) -> dict[str, Any]:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated = {}
    for field in fields:
        value = document.get(field)
        if value is None:
            continue
        result = translator.translate_text(
            str(value), target_lang=target_lang, model_type=DEEPL_MODEL_TYPE
        )
        translated[field] = result.text
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "translations": translated,
    }
