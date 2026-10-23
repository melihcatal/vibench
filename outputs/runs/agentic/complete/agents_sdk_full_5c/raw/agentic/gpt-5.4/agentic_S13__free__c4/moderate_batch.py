from __future__ import annotations

from typing import Iterable

from safety_models import BatchModerationResult
from moderate_text import moderate_text


def moderate_batch(messages: Iterable[str]) -> BatchModerationResult:
    decisions = [moderate_text(message) for message in messages]
    return BatchModerationResult(decisions=decisions, provider="azure_ai_content_safety")
