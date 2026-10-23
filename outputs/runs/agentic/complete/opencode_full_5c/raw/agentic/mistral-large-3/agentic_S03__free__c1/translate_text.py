from typing import Optional
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    client = TranslationClient()
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )
    return client.translate_text(text, normalized_target, normalized_source)
