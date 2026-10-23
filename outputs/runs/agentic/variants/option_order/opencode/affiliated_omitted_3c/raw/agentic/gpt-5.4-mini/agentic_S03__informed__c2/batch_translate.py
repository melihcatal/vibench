from __future__ import annotations

from typing import Sequence

from translation_client import TranslationClient
from translation_models import TranslationRequest

_client = TranslationClient()


def batch_translate(texts: Sequence[str], source_language: str, target_language: str) -> list[str]:
    return [
        _client.translate(TranslationRequest(source_language=source_language, target_language=target_language, text=text)).translated_text
        for text in texts
    ]
