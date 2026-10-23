from google.cloud import translate_v3
from translation_client import get_translation_client

def translate_dictionary_values(data: dict, target_language: str, source_language: str = "en") -> dict:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = get_translation_client()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}/locations/global"

    values_to_translate = [str(v) for v in data.values()]
    original_keys = list(data.keys())

    if not values_to_translate:
        return data

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": values_to_translate,
            "target_language_code": target_language,
            "source_language_code": source_language,
        }
    )

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = {}
    for i, key in enumerate(original_keys):
        translated_dict[key] = translated_values[i]

    return translated_dict
