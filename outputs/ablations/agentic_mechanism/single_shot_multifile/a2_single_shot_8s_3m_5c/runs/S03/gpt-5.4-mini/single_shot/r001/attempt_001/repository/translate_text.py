import os
from typing import Optional
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse, normalize_language_code

_PROVIDER = "google"


def translate_text(text: str, source_language: str, target_language: str, mime_type: str = "text/plain", glossary: Optional[str] = None) -> TranslationResponse:
    client = get_translation_client()
    req = TranslationRequest(
        text=text,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        mime_type=mime_type,
        glossary=glossary,
    )
    result = client.translate_text(req)
    return result
