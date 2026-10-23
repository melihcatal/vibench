import os
from typing import Iterable, List, Optional

from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_text


DEFAULT_SOURCE_LANG = os.getenv("TRANSLATION_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANG", "en")


def batch_translate(texts: Iterable[str], source_language: Optional[str] = None, target_language: Optional[str] = None) -> BatchTranslationResult:
    client = get_translation_client()
    request = BatchTranslationRequest(
        texts=[normalize_text(text) for text in texts],
        source_language=source_language or DEFAULT_SOURCE_LANG,
        target_language=target_language or DEFAULT_TARGET_LANG,
    )
    return client.batch_translate(request)


__all__ = ["batch_translate"]
