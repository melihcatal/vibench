from translation_client import get_translation_client
from typing import Dict, Any


def translate_dictionary_values(
    data: Dict[str, str], target_language_code: str, source_language_code: str = "en"
) -> Dict[str, str]:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = get_translation_client()
    project_id = ""  # Replace with your Google Cloud Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    original_keys = list(data.keys())
    values_to_translate = list(data.values())

    if not values_to_translate:
        return {}

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": values_to_translate,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translated_data = {}
    for i, key in enumerate(original_keys):
        translated_data[key] = response.translations[i].translated_text

    return translated_data
