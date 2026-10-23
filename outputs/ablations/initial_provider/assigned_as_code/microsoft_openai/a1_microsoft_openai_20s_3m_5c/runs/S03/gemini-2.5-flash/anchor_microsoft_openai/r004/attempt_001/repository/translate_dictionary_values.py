from typing import Dict
from translation_client import AzureTranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(data: Dict[str, str], source_language: str, target_language: str, config: dict = None) -> DictionaryTranslationResponse:
    config = config or {}
    client = AzureTranslationClient(api_key=config.get("api_key"), region=config.get("region"))
    request = DictionaryTranslationRequest(data=data, source_language=source_language, target_language=target_language)
    response = client.translate_dictionary_values(request)
    return response
