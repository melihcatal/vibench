from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, parent_path
from translation_models import coerce_language, normalize_mapping_values


def translate_dictionary_values(values, source_language: str, target_language: str):
    normalized = normalize_mapping_values(values)
    keys = list(normalized.keys())
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [normalized[key] for key in keys],
            "mime_type": "text/plain",
            "source_language_code": coerce_language(source_language),
            "target_language_code": coerce_language(target_language),
        }
    )
    translated = [item.translated_text for item in response.translations]
    return {key: translated[index] for index, key in enumerate(keys)}
