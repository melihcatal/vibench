import requests
from typing import Dict
from translation_client import YANDEX_FOLDER_ID, YANDEX_API_KEY, YANDEX_TRANSLATE_URL

def translate_dictionary(
    data: Dict[str, str],
    target_language: str,
    source_language: str = 'en'
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary using Yandex.Cloud Translate API.

    Args:
        data: The dictionary with string values to translate.
        target_language: The target language code.
        source_language: The source language code.

    Returns:
        A new dictionary with the same keys but translated values.
    """
    if not all([YANDEX_FOLDER_ID, YANDEX_API_KEY]):
        raise ValueError("Yandex.Cloud credentials are not set in environment variables.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    keys = list(data.keys())
    values_to_translate = list(data.values())

    body = {
        "targetLanguageCode": target_language,
        "sourceLanguageCode": source_language,
        "texts": values_to_translate,
        "folderId": YANDEX_FOLDER_ID,
    }

    response = requests.post(YANDEX_TRANSLATE_URL, json=body, headers=headers)
    response.raise_for_status()

    translations = response.json().get('translations', [])
    translated_values = [item['text'] for item in translations]

    if len(keys) != len(translated_values):
        raise ValueError("Mismatch between number of keys and translated values.")

    return dict(zip(keys, translated_values))
