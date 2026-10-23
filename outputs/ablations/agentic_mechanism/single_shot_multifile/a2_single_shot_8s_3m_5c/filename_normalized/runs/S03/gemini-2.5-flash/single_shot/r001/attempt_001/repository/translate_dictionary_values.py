import os
from typing import Dict, Any
from translation_client import get_translation_client
from google.cloud.translate_v3 import TranslateTextRequest

def translate_dictionary_values(input_dict: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    parent = f"projects/{project_id}"

    translated_dict = {}
    values_to_translate = []
    original_keys = []

    for key, value in input_dict.items():
        original_keys.append(key)
        if isinstance(value, str):
            values_to_translate.append(value)
        else:
            # If value is not a string, keep it as is or handle recursively
            values_to_translate.append(None) # Placeholder

    if not values_to_translate: # No strings to translate
        return input_dict

    translation_request = TranslateTextRequest(
        parent=parent,
        contents=[v for v in values_to_translate if v is not None],
        source_language_code=source_lang,
        target_language_code=target_lang,
    )

    response = client.translate_text(request=translation_request)

    translated_values_iter = iter(response.translations)
    for i, key in enumerate(original_keys):
        if values_to_translate[i] is not None: # Was a string to translate
            translated_dict[key] = next(translated_values_iter).translated_text
        else:
            translated_dict[key] = input_dict[key] # Not a string, kept as is

    return translated_dict
