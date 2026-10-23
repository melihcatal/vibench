from google.cloud import translate_v3 as translate
from typing import Dict, Any

def translate_dictionary_values(
    project_id: str,
    data: Dict[str, str],
    source_language_code: str,
    target_language_code: str,
) -> Dict[str, str]:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    keys = list(data.keys())
    values_to_translate = list(data.values())

    if not values_to_translate:
        return {}

    response = client.translate_text(
        parent=parent,
        contents=values_to_translate,
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = {}
    for i, key in enumerate(keys):
        translated_dict[key] = translated_values[i]

    return translated_dict
