from typing import Dict
from translation_client import get_translate_client
from translation_models import TranslationRequest

def translate_dictionary_values(input_dict: Dict[str, str], source_language_code: str, target_language_code: str) -> Dict[str, str]:
    client = get_translate_client()
    translated_dict = {}
    for key, value in input_dict.items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_dict[key] = response['TranslatedText']
    return translated_dict
