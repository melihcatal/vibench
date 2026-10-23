from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, TranslationResponse
from typing import Dict, Any


def translate_dictionary_values(
    dictionary: Dict[str, str], target_language: str, source_language: str = None
) -> Dict[str, str]:
    client = GoogleTranslationClient()
    translated_dict = {}
    values_to_translate = list(dictionary.values())

    if not values_to_translate:
        return translated_dict

    request = TranslationRequest(
        text=values_to_translate,
        target_language=target_language,
        source_language=source_language,
    )
    response = client.translate(request)

    translated_values = response.translated_text

    for i, key in enumerate(dictionary.keys()):
        translated_dict[key] = translated_values[i]

    return translated_dict
