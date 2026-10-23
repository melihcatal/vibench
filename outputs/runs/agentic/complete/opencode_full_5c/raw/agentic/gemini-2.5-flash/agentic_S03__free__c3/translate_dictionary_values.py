from translation_client import get_translation_client
from translation_models import get_project_id, get_location
from typing import Dict, Any


def translate_dict_values(
    data: Dict[str, str], target_language: str, source_language: str = ""
) -> Dict[str, str]:
    """Translates the string values of a dictionary using Google Cloud Translation V3, preserving keys.

    Args:
        data: A dictionary where values are strings to be translated.
        target_language: The language to translate the values to (e.g., "es" for Spanish).
        source_language: The language of the values. If not specified, auto-detected.

    Returns:
        A new dictionary with the same keys and translated string values.
    """
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    original_keys = list(data.keys())
    values_to_translate = [str(value) for value in data.values()]

    if not values_to_translate:
        return {}

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_data = {}
    for i, key in enumerate(original_keys):
        translated_data[key] = response.translations[i].translated_text

    return translated_data
