import os
from google.cloud import translate_v3

def translate_dictionary_values(
    project_id: str,
    data_dict: dict[str, str],
    target_language: str,
    source_language: str = "en",
) -> dict[str, str]:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    if not data_dict:
        return {}

    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    original_keys = list(data_dict.keys())
    original_values = [data_dict[key] for key in original_keys]

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": original_values,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = {
        original_keys[i]: translated_values[i] for i in range(len(original_keys))
    }
    return translated_dict

