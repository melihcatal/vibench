from typing import Dict, Optional
from translation_client import DeepLTranslationClient
from translation_models import TranslationRequest


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using DeepL API.
    """
    client = DeepLTranslationClient()
    translated_dict = {}

    for key, value in dictionary.items():
        request = TranslationRequest(
            text=value, target_language=target_language, source_language=source_language
        )
        response = client.translate_text(request)
        translated_dict[key] = response.translated_text

    return translated_dict
