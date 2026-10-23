from typing import Dict

from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, normalize_dictionary_response


def translate_dictionary_values(data: Dict[str, str], source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> Dict[str, str]:
    client = get_translation_client()
    request = DictionaryTranslationRequest(data=data, source_language=source_language, target_language=target_language)
    response = client.translate_dictionary_values(request=request, model=model)
    normalized = normalize_dictionary_response(response)
    return normalized.data
