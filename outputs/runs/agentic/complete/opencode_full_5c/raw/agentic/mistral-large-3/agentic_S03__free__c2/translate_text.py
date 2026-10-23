from typing import Dict, List, Optional
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """Translate a single text string using Google Cloud Translation API."""
    client = TranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )
    return client.translate_text(text, target_language, source_language)
