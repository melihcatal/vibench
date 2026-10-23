import os
from typing import Dict, Any
from translation_client import get_translation_client

def translate_dict_values(data: Dict[str, Any], target_language: str, source_language: str = "en") -> Dict[str, Any]:
    """Translates string values in a dictionary while preserving keys using Google Cloud Translation."""
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    values_to_translate = []
    keys_with_string_values = []

    for key, value in data.items():
        if isinstance(value, str):
            values_to_translate.append(value)
            keys_with_string_values.append(key)
        # Extend this logic if you need to handle nested dictionaries or lists of strings

    if not values_to_translate:
        return data.copy() # No strings to translate, return a copy of original

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_data = data.copy()
    for i, translation in enumerate(response.translations):
        original_key = keys_with_string_values[i]
        translated_data[original_key] = translation.translated_text

    return translated_data

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # data_to_translate = {
    #     "title": "Product Name",
    #     "description": "This is a great product.",
    #     "price": 100.00,
    #     "tags": ["electronic", "gadget"]
    # }
    # target_lang = "fr"
    # translated_dict = translate_dict_values(data_to_translate, target_lang)
    # print(f"Original Dict: {data_to_translate}")
    # print(f"Translated Dict ({target_lang}): {translated_dict}")
    pass
