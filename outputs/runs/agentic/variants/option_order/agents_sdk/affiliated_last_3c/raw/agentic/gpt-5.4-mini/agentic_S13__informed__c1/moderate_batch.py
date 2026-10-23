from __future__ import annotations

from typing import Iterable, List

from safety_models import BatchModerationResult, SafetyModerationRequest, SafetyModerationDecision
from moderate_text import moderate_text


def moderate_batch(messages: Iterable[str]) -> BatchModerationResult:
    decisions: List[SafetyModerationDecision] = [moderate_text(SafetyModerationRequest(text=message)) for message in messages]
    return BatchModerationResult(decisions=decisions, provider="azure-ai-content-safety")
