from google.cloud import translate_v3
from translation_client import get_translation_client
from typing import Dict, Any

def translate_dict_values(data: Dict[str, str], target_language: str, source_language: str = None) -> Dict[str, str]:
    """Translates string values in a dictionary while preserving keys using Google Cloud Translation."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    # Extract values to translate
    values_to_translate = [v for v in data.values() if isinstance(v, str)]
    original_keys = list(data.keys())

    if not values_to_translate:
        return data

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": values_to_translate,
            "target_language_code": target_language,
            "source_language_code": source_language,
            "mime_type": "text/plain",
        }
    )

    translated_values = [translation.translated_text for translation in response.translations]

    # Reconstruct the dictionary with translated values
    translated_data = {}
    translated_idx = 0
    for key in original_keys:
        if isinstance(data[key], str):
            translated_data[key] = translated_values[translated_idx]
            translated_idx += 1
        else:
            translated_data[key] = data[key] # Preserve non-string values

    return translated_data

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # my_dict = {"greeting": "Hello", "farewell": "Goodbye", "number": 123}
    # translated_dict = translate_dict_values(my_dict, "fr", "en")
    # print(f"Translated Dictionary: {translated_dict}")
    pass
