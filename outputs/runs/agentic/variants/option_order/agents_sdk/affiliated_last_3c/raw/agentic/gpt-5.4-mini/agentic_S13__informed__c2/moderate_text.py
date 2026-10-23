from __future__ import annotations

from safety_client import get_client
from safety_models import ModerationRequest


def moderate_text(text: str, language: str | None = None):
    client = get_client()
    return client.moderate(ModerationRequest(text=text, language=language))
