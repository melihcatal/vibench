from __future__ import annotations

from translation_client import TranslationClient
from translation_models import normalize_dictionary_values


def translate_dictionary_values(
    values: dict[str, object], source_language: str, target_language: str
) -> dict[str, str]:
    normalized = normalize_dictionary_values(values)
    keys = list(normalized.keys())
    payloads = TranslationClient().translate_many(
        texts=[normalized[key] for key in keys],
        source_language=source_language,
        target_language=target_language,
    )
    return {key: payload["translatedText"] for key, payload in zip(keys, payloads)}
