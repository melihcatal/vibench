from __future__ import annotations

from typing import Iterable, List

from safety_client import get_client
from safety_models import BatchModerationResult, ModerationRequest


def moderate_batch(messages: Iterable[str], language: str | None = None) -> BatchModerationResult:
    client = get_client()
    decisions = [client.moderate(ModerationRequest(text=message, language=language)) for message in messages]
    return BatchModerationResult(decisions=decisions)
