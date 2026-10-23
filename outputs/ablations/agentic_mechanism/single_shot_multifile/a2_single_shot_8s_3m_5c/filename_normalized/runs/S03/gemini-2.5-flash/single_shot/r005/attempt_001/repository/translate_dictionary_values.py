import os
from typing import Dict, Any
from translation_client import get_amazon_translate_client

def translate_dict_values(
    data_dict: Dict[str, Any],
    source_language_code: str,
    target_language_code: str,
    key_to_translate: str
) -> Dict[str, Any]:
    client = get_amazon_translate_client()
    translated_dict = data_dict.copy()

    if key_to_translate in data_dict and isinstance(data_dict[key_to_translate], str):
        text_to_translate = data_dict[key_to_translate]
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_dict[key_to_translate] = response['TranslatedText']
    return translated_dict
