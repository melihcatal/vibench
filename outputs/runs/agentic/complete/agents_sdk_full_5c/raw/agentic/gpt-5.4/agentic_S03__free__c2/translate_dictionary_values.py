from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_PROVIDER, get_google_translate_client
from translation_models import TranslationResult, normalize_mapping_values


def translate_dictionary_values(data: dict[str, object], source_language: str | None, target_language: str) -> dict[str, TranslationResult]:
    normalized = normalize_mapping_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]

    client = get_google_translate_client()
    response = client.translate(
        values,
        source_language=source_language,
        target_language=target_language,
        format_="text",
    )
    items = response if isinstance(response, list) else [response]
    return {
        key: TranslationResult(
            text=item["translatedText"],
            detected_source_language=item.get("detectedSourceLanguage"),
            provider=GOOGLE_TRANSLATE_PROVIDER,
            model="google-cloud-translate-v2",
        )
        for key, item in zip(keys, items)
    }
