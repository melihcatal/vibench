from typing import Dict, Mapping

from translation_client import (
    get_source_language,
    get_target_language,
    get_translation_client,
)
from translation_models import TranslationResponse, normalize_mapping_values


def translate_dictionary_values(
    values: Mapping[str, str], source_language: str, target_language: str
) -> Dict[str, TranslationResponse]:
    client = get_translation_client()
    normalized = normalize_mapping_values(values)
    translated = {}
    for key, value in normalized.items():
        result = client.translate_text(
            value,
            source_lang=get_source_language(source_language),
            target_lang=get_target_language(target_language),
        )
        translated[key] = TranslationResponse(
            translated_text=result.text,
            detected_source_language=getattr(result, "detected_source_lang", None),
            provider="deepl",
        )
    return translated
