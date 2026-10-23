from __future__ import annotations

from typing import Sequence

from translation_client import get_client
from translation_models import BatchTranslationRequest


def batch_translate(texts: Sequence[str], source_language: str, target_language: str):
    client = get_client()
    return client.batch_translate(
        BatchTranslationRequest(
            texts=texts,
            source_language=source_language,
            target_language=target_language,
        )
    )
