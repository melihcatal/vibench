from typing import Any, Dict

from translation_client import extract_google_translations, translate_with_google
from translation_models import normalize_mapping_values


def translate_dictionary_values(
    data: Dict[str, Any], source_language: str | None, target_language: str
) -> Dict[str, str]:
    normalized = normalize_mapping_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    payload = translate_with_google(
        texts=values,
        source_language=source_language,
        target_language=target_language,
        fmt="text",
        model="nmt",
    )
    translated_items = extract_google_translations(payload)
    translated_values = [item.get("translatedText", "") for item in translated_items]
    return dict(zip(keys, translated_values))
