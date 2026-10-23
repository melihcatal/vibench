from typing import Dict, Any
from translation_models import DictionaryTranslationRequest
from translation_client import get_openai_client, translate_dictionary_content


def translate_dictionary_values(
    data: Dict[str, Any],
    source_language: str = "auto",
    target_language: str = "en",
    translate_keys: bool = False,
) -> Dict[str, Any]:
    client = get_openai_client()
    request = DictionaryTranslationRequest(
        data=data,
        source_language=source_language,
        target_language=target_language,
        translate_keys=translate_keys,
    )
    return translate_dictionary_content(client, request)
