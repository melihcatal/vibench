from __future__ import annotations

from translation_client import translate_request
from translation_models import TranslationRequest


def translate_text(text: str, source_language: str, target_language: str) -> str:
    return translate_request(TranslationRequest(text=text, source_language=source_language, target_language=target_language))
