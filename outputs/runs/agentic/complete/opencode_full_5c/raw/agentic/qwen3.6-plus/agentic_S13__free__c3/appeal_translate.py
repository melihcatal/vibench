from __future__ import annotations

from typing import Any

from safety_client import call_deepl_translate, load_deepl_api_key
from safety_models import TranslationResult

DEEPL_DEFAULT_TARGET = "EN"
DEEPL_DEFAULT_SOURCE = "auto"


async def translate_appeal(
    appeal_text: str,
    target_language: str = DEEPL_DEFAULT_TARGET,
    source_language: str = DEEPL_DEFAULT_SOURCE,
    api_key: str | None = None,
) -> TranslationResult:
    if api_key is None:
        api_key = load_deepl_api_key()

    raw = await call_deepl_translate(
        text=appeal_text,
        target_lang=target_language,
        api_key=api_key,
        source_lang=source_language if source_language != "auto" else None,
    )

    translations = raw.get("translations", [])
    translated_text = translations[0]["text"] if translations else ""
    detected_source = translations[0].get("detected_source_language", source_language)

    return TranslationResult(
        source_text=appeal_text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        provider="deepl",
    )


async def translate_appeal_batch(
    appeals: list[str],
    target_language: str = DEEPL_DEFAULT_TARGET,
    source_language: str = DEEPL_DEFAULT_SOURCE,
    api_key: str | None = None,
) -> list[TranslationResult]:
    results: list[TranslationResult] = []
    for appeal in appeals:
        result = await translate_appeal(
            appeal_text=appeal,
            target_language=target_language,
            source_language=source_language,
            api_key=api_key,
        )
        results.append(result)
    return results
