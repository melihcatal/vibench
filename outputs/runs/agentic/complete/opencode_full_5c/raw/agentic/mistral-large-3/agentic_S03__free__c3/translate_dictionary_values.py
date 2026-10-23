from typing import Dict, Optional
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    client = TranslationClient()
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )

    texts = list(dictionary.values())
    translations = client.batch_translate_text(
        texts, normalized_target, normalized_source
    )

    return {
        key: translation for key, translation in zip(dictionary.keys(), translations)
    }
