import os
import requests

DEEPL_API_BASE_URL = "https://api-free.deepl.com/v2/" # Or https://api.deepl.com/v2/ for pro

def translate_dictionary_values(data: dict, source_language: str, target_language: str) -> dict:
    """
    Translates dictionary values while preserving keys using DeepL API.

    Args:
        data: The dictionary whose values are to be translated.
        source_language: The language of the input values (e.g., "en", "fr").
        target_language: The language to translate the values into (e.g., "es", "de").

    Returns:
        A new dictionary with translated values, preserving the original keys.
    """
    translated_data = {}
    auth_key = os.environ.get("DEEPL_API_KEY")

    for key, value in data.items():
        if isinstance(value, str):
            headers = {"Authorization": f"DeepL-Auth-Key {auth_key}"}
            payload = {
                "text": [value],
                "source_lang": source_language.upper(),
                "target_lang": target_language.upper(),
            }
            response = requests.post(f"{DEEPL_API_BASE_URL}translate", headers=headers, json=payload)
            response.raise_for_status()
            translated_value = response.json()["translations"][0]["text"]
            translated_data[key] = translated_value
        else:
            translated_data[key] = value
            
    return translated_data
