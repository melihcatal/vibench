from translation_client import AzureTranslatorClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
import dataclasses
from typing import List, Dict, Any


@dataclasses.dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, str]
    detected_languages: Dict[str, str] = None


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = AzureTranslatorClient()

    original_keys = list(request.data.keys())
    original_values = list(request.data.values())

    response = client.client.translate(
        text_elements=original_values,
        to=[request.to_lang],
        from_parameter=request.from_lang,
    )

    translated_data = {}
    detected_languages = {}

    if response:
        for i, translation_item in enumerate(response):
            key = original_keys[i]
            if translation_item.translations:
                translated_data[key] = translation_item.translations[0].text
                detected_languages[key] = (
                    translation_item.detected_language.language
                    if translation_item.detected_language
                    else None
                )
            else:
                translated_data[key] = ""
                detected_languages[key] = None

    return DictionaryTranslationResponse(
        translated_data=translated_data, detected_languages=detected_languages
    )
