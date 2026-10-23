import os
from typing import Dict, Any
from translation_client import get_translation_client, get_location_path

def translate_dictionary_values(
    data: Dict[str, str],
    target_language_code: str,
    source_language_code: str = "",
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
) -> Dict[str, str]:
    """Translates string values in a dictionary using Google Cloud Translation API, preserving keys."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    if not data:
        return {}

    client = get_translation_client()
    location_path = get_location_path(project_id)

    original_keys = list(data.keys())
    values_to_translate = list(data.values())

    if not values_to_translate:
        return {}

    response = client.translate_text(
        request={
            "parent": location_path,
            "contents": values_to_translate,
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = dict(zip(original_keys, translated_values))
    return translated_dict
