import deepl
import os
from typing import Dict, Any, Optional
from translation_client import get_deepl_client

def translate_dict_values(data: Dict[str, Any], target_lang: str, source_lang: Optional[str] = None) -> Dict[str, Any]:
    """
    Translates string values in a dictionary while preserving keys using DeepL.
    This function will only translate top-level string values.
    """
    client = get_deepl_client()
    translated_data = {}
    texts_to_translate = []
    keys_order = []

    for key, value in data.items():
        if isinstance(value, str):
            texts_to_translate.append(value)
            keys_order.append(key)
        else:
            translated_data[key] = value # Preserve non-string values

    if texts_to_translate:
        translated_results = client.translate_text(
            texts_to_translate,
            target_lang=target_lang,
            source_lang=source_lang
        )
        for i, key in enumerate(keys_order):
            translated_data[key] = translated_results[i].text

    return translated_data

if __name__ == '__main__':
    # Example usage (ensure DEEPL_AUTH_KEY is set in environment variables)
    dict_to_translate = {
        "greeting": "Good morning!",
        "farewell": "See you later.",
        "number": 123,
        "status": True
    }
    target_language = "pt-BR"
    translated_dict = translate_dict_values(dict_to_translate, target_language)
    print(f"Original Dictionary: {dict_to_translate}")
    print(f"Translated Dictionary ({target_language}): {translated_dict}")
