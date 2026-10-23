import os
from typing import Dict, Any
from translation_client import get_translation_client

def translate_dictionary_values(
    data: Dict[str, Any], target_language: str, source_language: str = ""
) -> Dict[str, Any]:
    """Translates string values within a dictionary using Google Cloud Translation API,
    preserving keys.

    Args:
        data: A dictionary whose string values need to be translated.
        target_language: The language to translate the values to (e.g., 'es' for Spanish).
        source_language: The language of the input values (e.g., 'en' for English).
                         If not specified, Google will auto-detect.

    Returns:
        A new dictionary with translated string values.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable not set. "
            "Please set it to your Google Cloud Project ID."
        )

    parent = f"projects/{project_id}/locations/global"
    translated_data = {}
    texts_to_translate = []
    keys_order = []

    for key, value in data.items():
        if isinstance(value, str):
            texts_to_translate.append(value)
            keys_order.append(key)
            translated_data[key] = None  # Placeholder
        else:
            translated_data[key] = value  # Keep non-string values as is

    if texts_to_translate:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "target_language_code": target_language,
                "source_language_code": source_language if source_language else None,
            }
        )

        for i, translation in enumerate(response.translations):
            translated_data[keys_order[i]] = translation.translated_text

    return translated_data
