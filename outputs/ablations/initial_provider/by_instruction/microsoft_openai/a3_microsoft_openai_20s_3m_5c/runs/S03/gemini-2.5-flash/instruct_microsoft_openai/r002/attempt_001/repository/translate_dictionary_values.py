import os
from typing import Dict
from translation_client import OpenAITranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(dictionary: Dict[str, str], target_language: str, source_language: str = None) -> DictionaryTranslationResponse:
    """
    Translates dictionary values while preserving keys using OpenAI.
    """
    client = OpenAITranslationClient()
    request = DictionaryTranslationRequest(
        dictionary=dictionary,
        target_language=target_language,
        source_language=source_language
    )
    response = client.translate_dictionary_values(request)
    return response
