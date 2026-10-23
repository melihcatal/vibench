from __future__ import annotations

import os

import deepl

from messaging_models import normalize_text_payload


DEEPL_TARGET_LANG = os.getenv("DEEPL_TARGET_LANG", "EN-US")


def translate_payload_text(payload: dict, target_lang: str | None = None) -> dict[str, str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    text = normalize_text_payload(payload)
    target = target_lang or DEEPL_TARGET_LANG
    result = translator.translate_text(text, target_lang=target)
    return {
        "provider": "deepl",
        "target_lang": target,
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
    }
