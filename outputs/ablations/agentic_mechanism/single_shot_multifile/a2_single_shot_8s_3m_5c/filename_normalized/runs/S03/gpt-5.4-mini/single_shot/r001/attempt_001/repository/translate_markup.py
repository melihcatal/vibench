from typing import Optional
from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse, normalize_language_code

_PROVIDER = "google"


def translate_markup(markup: str, source_language: str, target_language: str, content_type: str = "text/html", glossary: Optional[str] = None) -> MarkupTranslationResponse:
    client = get_translation_client()
    req = MarkupTranslationRequest(
        markup=markup,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        content_type=content_type,
        glossary=glossary,
    )
    return client.translate_markup(req)
