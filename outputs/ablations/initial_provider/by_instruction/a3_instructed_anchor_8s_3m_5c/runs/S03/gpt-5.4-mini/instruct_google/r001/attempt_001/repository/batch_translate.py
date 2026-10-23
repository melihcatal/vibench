from google.cloud import translate_v3

from translation_client import get_translation_client, load_translation_config, location_path
from translation_models import normalize_text_list


def batch_translate_text(values, source_language, target_language):
    config = load_translation_config()
    client = get_translation_client()
    parent = location_path(config)
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": normalize_text_list(values),
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    return [item.translated_text for item in response.translations]
