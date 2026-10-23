from translation_client import get_translation_client
from typing import Dict, Any


def translate_dictionary_values(
    data: Dict[str, str],
    target_language: str,
    project_id: str,
    source_language: str = "",
) -> Dict[str, str]:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    original_keys = list(data.keys())
    texts_to_translate = list(data.values())

    if not texts_to_translate:
        return {}

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts_to_translate,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_values = [
        translation.translated_text for translation in response.translations
    ]

    translated_dict = {
        original_keys[i]: translated_values[i] for i in range(len(original_keys))
    }
    return translated_dict
