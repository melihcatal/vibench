from typing import Dict, Optional, Any
from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse, normalize_language_code

_PROVIDER = "google"


def translate_dictionary_values(values: Dict[str, str], source_language: str, target_language: str, glossary: Optional[str] = None) -> DictionaryTranslationResponse:
    client = get_translation_client()
    req = DictionaryTranslationRequest(
        values=dict(values),
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        glossary=glossary,
    )
    return client.translate_dictionary_values(req)
