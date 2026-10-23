from google.cloud import translate_v3

from translation_client import get_translation_client, load_translation_config, location_path
from translation_models import normalize_dict_values


def translate_dictionary_values(values, source_language, target_language):
    config = load_translation_config()
    client = get_translation_client()
    normalized = normalize_dict_values(values)
    keys = list(normalized.keys())
    response = client.translate_text(
        request={
            "parent": location_path(config),
            "contents": [normalized[key] for key in keys],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    return {key: translation.translated_text for key, translation in zip(keys, response.translations)}
