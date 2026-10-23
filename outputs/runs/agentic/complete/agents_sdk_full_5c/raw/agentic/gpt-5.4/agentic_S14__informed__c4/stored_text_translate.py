from __future__ import annotations

from typing import Optional

import deepl

from storage_models import TranslationResult


def translate_extracted_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    glossary_id: Optional[str] = None,
) -> TranslationResult:
    client = deepl.Translator(__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    if not client.auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")

    result = client.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        glossary=glossary_id,
    )
    detected_source = getattr(result, "detected_source_lang", None) or source_language
    return TranslationResult(
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        provider="deepl",
    )
