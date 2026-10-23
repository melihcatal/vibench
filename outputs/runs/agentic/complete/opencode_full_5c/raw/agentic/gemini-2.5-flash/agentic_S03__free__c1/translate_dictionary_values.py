import os
from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest
from typing import Dict

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> Dict[str, str]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    translated_dict = {}
    for key, value in request.dictionary.items():
        translated_value = client.translate_text(
            value, request.target_language, request.source_language
        )
        translated_dict[key] = translated_value
    return translated_dict
