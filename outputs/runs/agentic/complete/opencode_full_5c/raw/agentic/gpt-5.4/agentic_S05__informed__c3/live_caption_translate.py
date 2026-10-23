from __future__ import annotations

import os

import deepl


def translate_live_caption(
    text: str, target_language: str, source_language: str | None = None
) -> dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required for DeepL API")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return {
        "source_text": text,
        "translated_text": result.text,
        "detected_source_language": getattr(
            result, "detected_source_lang", source_language
        )
        or "",
        "target_language": target_language,
    }
