from __future__ import annotations

from translation_client import batch_translate_with_google
from translation_models import TranslationResult, coerce_dictionary_values


def translate_dictionary_values(
    data: dict[str, str],
    target_language: str,
    source_language: str | None = None,
) -> dict[str, TranslationResult]:
    normalized = coerce_dictionary_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    raws = batch_translate_with_google(
        texts=values,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return {
        key: TranslationResult(
            translated_text=raw["translatedText"],
            detected_source_language=raw.get("detectedSourceLanguage") or source_language,
            provider="google_translate",
            model="google-cloud-translate-v2",
            raw=raw,
        )
        for key, raw in zip(keys, raws)
    }
