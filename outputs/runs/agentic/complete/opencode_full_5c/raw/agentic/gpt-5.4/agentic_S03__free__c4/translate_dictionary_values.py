from __future__ import annotations

from translation_client import deepl_translate
from translation_models import normalize_dictionary_values, normalize_language_code


def translate_dictionary_values(
    values: dict[str, object], source_language: str | None, target_language: str
) -> dict[str, str]:
    normalized_values = normalize_dictionary_values(values)
    keys = list(normalized_values.keys())
    texts = [normalized_values[key] for key in keys]
    translations = deepl_translate(
        texts,
        normalize_language_code(target_language) or target_language,
        normalize_language_code(source_language),
    )
    return {key: item["text"] for key, item in zip(keys, translations, strict=True)}
