from __future__ import annotations

from speech_client import client
from speech_models import TranslationResult


def live_caption_translate(text: str, target_language: str = "es") -> TranslationResult:
    return client.translate_text(text=text, target_language=target_language)
