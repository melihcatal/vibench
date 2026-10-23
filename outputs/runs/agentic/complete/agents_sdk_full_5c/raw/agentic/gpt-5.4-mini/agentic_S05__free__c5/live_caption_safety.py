from __future__ import annotations

from speech_client import client
from speech_models import SafetyResult


def live_caption_safety(text: str) -> SafetyResult:
    return client.moderate_text(text)
