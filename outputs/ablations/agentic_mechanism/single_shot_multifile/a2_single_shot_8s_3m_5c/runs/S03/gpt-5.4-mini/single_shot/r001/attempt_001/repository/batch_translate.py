from typing import List, Optional
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_language_code

_PROVIDER = "google"


def batch_translate(texts: List[str], source_language: str, target_language: str, mime_type: str = "text/plain", glossary: Optional[str] = None) -> BatchTranslationResponse:
    client = get_translation_client()
    req = BatchTranslationRequest(
        texts=list(texts),
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        mime_type=mime_type,
        glossary=glossary,
    )
    return client.batch_translate(req)
