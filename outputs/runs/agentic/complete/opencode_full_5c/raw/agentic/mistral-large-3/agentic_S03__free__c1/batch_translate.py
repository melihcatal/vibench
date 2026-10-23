from typing import List, Optional
from translation_client import TranslationClient
from translation_models import normalize_language_code


def batch_translate(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    client = TranslationClient()
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )
    return client.batch_translate_text(texts, normalized_target, normalized_source)
