from __future__ import annotations

from typing import Iterable, List

from translation_client import batch_translate_request
from translation_models import BatchTranslationRequest


def batch_translate(texts: Iterable[str], source_language: str, target_language: str) -> List[str]:
    request = BatchTranslationRequest(texts=list(texts), source_language=source_language, target_language=target_language)
    return batch_translate_request(request)
