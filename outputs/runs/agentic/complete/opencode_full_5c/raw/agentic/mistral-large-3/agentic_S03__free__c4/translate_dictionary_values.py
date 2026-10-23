from typing import Dict, List, Optional
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """Translate dictionary values while preserving keys using Google Cloud Translation API."""
    client = TranslationClient()
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )
    values = list(dictionary.values())
    translated_values = client.batch_translate_text(
        values, normalized_target, normalized_source
    )
    return {key: translated_values[i] for i, key in enumerate(dictionary.keys())}
